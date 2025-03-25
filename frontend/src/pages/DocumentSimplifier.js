import React, { useState } from 'react';
import axios from 'axios';
import { getDocument, GlobalWorkerOptions } from 'pdfjs-dist/build/pdf';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.13.216/pdf.worker.min.js`;

const DocumentSimplifier = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [pineconeMessage, setPineconeMessage] = useState('');
    const [queryAnswer, setQueryAnswer] = useState('');
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');
    const [customQuery, setCustomQuery] = useState('');
    const [isPineconeFilled, setIsPineconeFilled] = useState(false);

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            setSelectedFile(file);
            setMessage('');
        } else {
            setMessage('Please select a valid file.');
        }
    };

    const extractTextFromPDF = async (file) => {
        const pdfData = await file.arrayBuffer();
        const pdfDoc = await getDocument({ data: pdfData }).promise;
        let text = '';
        for (let i = 1; i <= pdfDoc.numPages; i++) {
            const page = await pdfDoc.getPage(i);
            const textContent = await page.getTextContent();
            const pageText = textContent.items.map(item => item.str).join(' ');
            text += pageText + '\n';
        }
        return text.trim();
    };

    const handleFillPinecone = async () => {
        if (!selectedFile) {
            setMessage('Please select a file to upload.');
            return;
        }
        setLoading(true);
        try {
            const extractedText = await extractTextFromPDF(selectedFile);
            const formData = new FormData();
            formData.append('document_text', extractedText);

            const response = await axios.post('http://localhost:5000/api/fill-pinecone', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
            setPineconeMessage(JSON.stringify(response.data));
            setMessage('Pinecone index filled successfully!');
            setIsPineconeFilled(true);
        } catch (error) {
            setMessage('Error filling Pinecone index: ' + (error.response ? error.response.data.message : error.message));
        }
        setLoading(false);
    };

    const handleQueryLLM = async () => {
        if (!customQuery) {
            setMessage('Please enter a query.');
            return;
        }
        setLoading(true);
        try {
            const payload = {
                Query: customQuery
            };
            const response = await axios.post('http://localhost:5000/api/query-llm', payload, {
                headers: { 'Content-Type': 'application/json' },
            });
            setQueryAnswer(response.data.Response);
            setMessage('Query answered successfully!');
        } catch (error) {
            setMessage('Error processing your query: ' + (error.response ? error.response.data.message : error.message));
        }
        setLoading(false);
    };

    return (
        <div className="bg-gradient-to-r from-green-200 via-blue-200 to-purple-200 min-h-screen p-8 flex flex-col items-center" style={{ fontFamily: 'OpenDyslexic', lineHeight: '1.5' }}>
            <ToastContainer />
            <h1 className="text-4xl font-bold mb-8 text-blue-800 text-center">AI Powered RAG based Chat with Document</h1>
            {!isPineconeFilled && (
                <div className="mb-4 w-full max-w-md">
                    <input
                        type="file"
                        name="file"
                        accept=".pdf"
                        onChange={handleFileChange}
                        className="block w-full border border-gray-300 rounded-md p-2 mb-4"
                    />
                    <button
                        className="bg-gradient-to-r from-blue-400 to-blue-600 text-white py-2 px-4 rounded-lg shadow-lg hover:shadow-xl transition duration-300 ease-in-out"
                        onClick={handleFillPinecone}
                    >
                        {loading ? 'Processing...' : 'Fill Pinecone Index'}
                    </button>
                </div>
            )}
            {isPineconeFilled && (
                <div className="mb-4 w-full max-w-md">
                    <p className="mb-4">Pinecone index filled successfully! You may now enter your query:</p>
                    <input
                        type="text"
                        placeholder="Enter your query here..."
                        value={customQuery}
                        onChange={(e) => setCustomQuery(e.target.value)}
                        className="block w-full border border-gray-300 rounded-md p-2 mt-2 text-center shadow-md"
                    />
                    <button
                        className="bg-gradient-to-r from-blue-400 to-blue-600 text-white py-2 px-4 rounded-lg shadow-lg hover:shadow-xl transition duration-300 ease-in-out mt-4"
                        onClick={handleQueryLLM}
                    >
                        {loading ? 'Processing...' : 'Submit Query'}
                    </button>
                </div>
            )}
            {message && <p className="mt-4 text-red-600">{message}</p>}
            {queryAnswer && (
                <div className="mt-4 bg-white shadow-lg rounded-lg p-6 w-full max-w-4xl">
                    <h2 className="text-xl font-bold">Query Answer:</h2>
                    <p className="mt-2 whitespace-pre-wrap text-gray-700">{queryAnswer}</p>
                </div>
            )}
        </div>
    );
};

export default DocumentSimplifier;
