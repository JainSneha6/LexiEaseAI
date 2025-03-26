import React, { useState } from 'react';
import axios from 'axios';
import { getDocument, GlobalWorkerOptions } from 'pdfjs-dist/build/pdf';
import { jsPDF } from 'jspdf';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import ReactFlow, { MiniMap, Controls, Background, ReactFlowProvider } from 'reactflow';
import 'reactflow/dist/style.css';
import ReactMarkdown from "react-markdown";

GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${'2.13.216'}/pdf.worker.min.js`;

const MindMapGenerator = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [simplifiedText, setSimplifiedText] = useState('');
    const [importantPoints, setImportantPoints] = useState([]);
    const [loadingText, setLoadingText] = useState(false);
    const [loadingMindmap, setLoadingMindmap] = useState(false);
    const [message, setMessage] = useState('');

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            console.log('Selected file:', file);
            setSelectedFile(file);
            setMessage('');
            // Reset previous states
            setSimplifiedText('');
            setImportantPoints([]);
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

    const handleGenerateNotes = async () => {
        if (!selectedFile) {
            setMessage('Please select a file to upload.');
            return;
        }
        try {
            setLoadingText(true);
            const extractedText = await extractTextFromPDF(selectedFile);
            console.log('Extracted text for notes:', extractedText);

            const dataToSend = { extracted_content: extractedText };

            const response = await axios.post('http://localhost:5000/api/generate-notes', dataToSend, {
                headers: { 'Content-Type': 'application/json' },
            });

            setSimplifiedText(response.data.LLM_Response);
            setMessage('Notes generated successfully!');
        } catch (error) {
            console.error('Error generating notes:', error.response ? error.response.data : error.message);
            setMessage('Error generating notes: ' + (error.response ? error.response.data.message : error.message));
        }
        setLoadingText(false);
    };

    const handleGenerateMindMap = async () => {
        if (!selectedFile) {
            setMessage('Please select a file to upload.');
            return;
        }
        try {
            setLoadingMindmap(true);
            const extractedText = await extractTextFromPDF(selectedFile);
            console.log('Extracted text for mind map:', extractedText);

            const dataToSend = { extracted_content: simplifiedText };

            const response = await axios.post('http://localhost:5000/api/generate-mindmap', dataToSend, {
                headers: { 'Content-Type': 'application/json' },
            });

            console.log('Response from server:', response.data);
            const combined_response_mindmap = response.data;
            setImportantPoints([
                combined_response_mindmap.LLM_Answer1,
                combined_response_mindmap.LLM_Answer2,
                combined_response_mindmap.LLM_Answer3
            ]);
            setMessage('Mind Map generated successfully!');
        } catch (error) {
            console.error('Error generating mind map:', error.response ? error.response.data : error.message);
            setMessage('Error generating mind map: ' + (error.response ? error.response.data.message : error.message));
        }
        setLoadingMindmap(false);
    };

    const handleDownloadPDF = () => {
        if (!simplifiedText) {
            setMessage('No simplified text to download.');
            return;
        }
        const doc = new jsPDF();
        doc.setFontSize(12);
        const lines = doc.splitTextToSize(simplifiedText, 190);
        let yPosition = 10;
        const lineHeight = 10;

        lines.forEach((line) => {
            if (yPosition + lineHeight > doc.internal.pageSize.height - 10) {
                doc.addPage();
                yPosition = 10;
            }
            doc.text(line, 10, yPosition);
            yPosition += lineHeight;
        });

        doc.save('simplified_text.pdf');
    };

    return (
        <div className="bg-gradient-to-r from-green-200 via-blue-200 to-purple-200 min-h-screen p-8 flex flex-col items-center" style={{ fontFamily: 'OpenDyslexic', lineHeight: '1.5' }}>
            <ToastContainer />
            <h1 className="text-4xl font-bold mb-8 text-blue-800 text-center">AI-Powered Notes and MindMap Generator</h1>

            <div className="mb-4 w-full max-w-md">
                <input
                    type="file"
                    name='file'
                    accept=".pdf"
                    onChange={handleFileChange}
                    className="block w-full border border-gray-300 rounded-md p-2 mb-4"
                />
            </div>

            <div className="flex space-x-4 mb-4">
                <button
                    className="bg-blue-500 text-white py-2 px-4 rounded-lg shadow-lg hover:shadow-xl transition duration-300 ease-in-out"
                    onClick={handleGenerateNotes}
                    disabled={loadingText}
                >
                    {loadingText ? 'Processing...' : 'Generate Notes'}
                </button>

                <button
                    className="bg-purple-500 text-white py-2 px-4 rounded-lg shadow-lg hover:shadow-xl transition duration-300 ease-in-out"
                    onClick={handleGenerateMindMap}
                    disabled={loadingMindmap}
                >
                    {loadingMindmap ? 'Processing...' : 'Generate Mind Map'}
                </button>
            </div>

            {message && <p className="mt-4 text-red-600">{message}</p>}

            {simplifiedText && (
                <div className="mt-4 bg-white shadow-lg rounded-lg p-6 w-full max-w-4xl">
                    <h2 className="text-xl font-bold mb-8">Simplified Text:</h2>
                    <ReactMarkdown>{String(simplifiedText)}</ReactMarkdown>
                    <button
                        className="bg-green-500 text-white py-2 px-4 rounded-lg mt-4 hover:bg-green-600 transition duration-300 ease-in-out"
                        onClick={handleDownloadPDF}
                    >
                        Download Notes
                    </button>
                </div>
            )}

            {Array.isArray(importantPoints) && importantPoints.length > 0 && (
                <div className="mt-4 w-full max-w-4xl">
                    <h2 className="text-xl font-bold">Mind Map:</h2>
                    <MindMap importantPoints={importantPoints} />
                </div>
            )}
        </div>
    );
};

const MindMap = ({ importantPoints }) => {
    const { nodes, edges } = createMindMapElements(importantPoints);

    return (
        <div style={{ height: '500px', width: '100%' }}>
            <ReactFlowProvider>
                <ReactFlow
                    nodes={nodes}
                    edges={edges}
                    snapToGrid={true}
                    snapGrid={[15, 15]}
                    style={{ background: '#f0f0f0' }}
                >
                    <MiniMap />
                    <Controls />
                    <Background color="#aaa" gap={16} />
                </ReactFlow>
            </ReactFlowProvider>
        </div>
    );
};

const createMindMapElements = (points) => {
    const nodes = [];
    const edges = [];
    const centerX = 500;
    const centerY = 300;
    const radius = 400;

    points.forEach((point, index) => {
        const nodeId = `${index + 1}`;
        const angle = (index / points.length) * 2 * Math.PI;
        const xPos = centerX + radius * Math.cos(angle);
        const yPos = centerY + radius * Math.sin(angle);
        nodes.push({
            id: nodeId,
            data: { label: point },
            position: { x: xPos, y: yPos },
            style: {
                width: 350,
                height: 150,
                backgroundColor: '#b2ebf2',
                backgroundImage: 'linear-gradient(to right, #e0f7fa, #b2ebf2)',
                border: '2px solid #00796b',
                borderRadius: '15px',
                boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.1)',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                textAlign: 'center',
                fontSize: '18px',
                padding: '25px',
                wordWrap: 'break-word',
            }
        });

        if (index > 0) {
            edges.push({
                id: `e${index}-0`,
                source: '0',
                target: nodeId,
                animated: true,
                type: 'bezier',
                style: { stroke: '#00796b' }
            });
        }
    });

    nodes.push({
        id: '0',
        data: { label: 'Central Idea' },
        position: { x: centerX, y: centerY },
        style: {
            width: 350,
            height: 150,
            backgroundColor: '#fff59d',
            border: '2px solid #fbc02d',
            borderRadius: '20px',
            boxShadow: '0px 4px 12px rgba(0, 0, 0, 0.2)',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            textAlign: 'center',
            fontSize: '20px',
            padding: '30px',
            fontWeight: 'bold',
        }
    });

    return { nodes, edges };
};

export default MindMapGenerator;
