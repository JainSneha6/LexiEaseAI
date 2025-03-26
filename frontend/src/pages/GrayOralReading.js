import React, { useState, useEffect } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import axios from 'axios';
import 'react-toastify/dist/ReactToastify.css';

const GrayOralReadingTest = () => {
  const [isReading, setIsReading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [audioBlob, setAudioBlob] = useState(null);
  const [readingTime, setReadingTime] = useState(0);
  const [isTestCompleted, setIsTestCompleted] = useState(false);
  const [readingSpeed, setReadingSpeed] = useState(0);
  const [fluencyRating, setFluencyRating] = useState(null);
  const [startTime, setStartTime] = useState(null);

  // State to store the combined list of passages
  const [passagesList, setPassagesList] = useState([]);
  // Current index of the passage being displayed
  const [currentIndex, setCurrentIndex] = useState(0);

  // Fetch passages from the backend and merge them into one array
  useEffect(() => {
    axios
      .get('http://localhost:5000/api/passages')
      .then((response) => {
        // Merge all arrays (easy, medium, hard) into one list.
        const merged = [
          ...response.data.easy,
          ...response.data.medium,
          ...response.data.hard,
        ];
        setPassagesList(merged);
      })
      .catch((error) => {
        console.error('Error fetching passages:', error);
        toast.error('Error fetching passages from backend.');
      });
  }, []);

  // The current passage text is taken from the "MEDIUM" key (adjust if needed)
  const currentPassage = passagesList[currentIndex]
    ? passagesList[currentIndex].MEDIUM
    : '';

  const handleStartReading = async () => {
    if (!currentPassage) {
      toast.error('No passage available to read.');
      return;
    }
    setIsReading(true);
    setStartTime(Date.now());

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      setMediaRecorder(recorder);

      let chunks = [];
      recorder.ondataavailable = (event) => {
        chunks.push(event.data);
      };

      recorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/wav' });
        setAudioBlob(blob);
        setIsRecording(false);
      };

      recorder.onerror = (event) => {
        console.error('MediaRecorder error:', event.error);
        toast.error('MediaRecorder error occurred.');
      };

      recorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
      toast.error('Error accessing microphone. Please check your permissions.');
      setIsReading(false);
    }
  };

  const handleFinishReading = () => {
    setIsReading(false);
    const timeTaken = (Date.now() - startTime) / 1000;
    setReadingTime(timeTaken);
    setIsTestCompleted(true);

    const wordsInPassage = currentPassage.split(' ').length;
    const speed = (wordsInPassage / (timeTaken / 60)).toFixed(2);
    setReadingSpeed(speed);

    if (mediaRecorder) {
      mediaRecorder.stop();
    } else {
      toast.error('Recording not started correctly.');
    }
  };

  const uploadAudioToBackend = async () => {
    if (!audioBlob) {
      toast.error('No audio recorded!');
      return;
    }
    const formData = new FormData();
    formData.append('audio', audioBlob, 'reading-test.wav');

    try {
      const response = await axios.post('http://localhost:5000/api/upload-audio', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setFluencyRating(response.data.fluency_rating.Fluency);
      console.log(response.data);
      toast.success('Audio uploaded successfully!');
    } catch (error) {
      console.error('Error uploading audio:', error.response ? error.response.data : error.message);
      toast.error('Error uploading audio!');
    }
  };

  // When the test is completed and audioBlob is available, upload audio to backend.
  useEffect(() => {
    if (isTestCompleted && audioBlob) {
      uploadAudioToBackend();
    }
  }, [isTestCompleted, audioBlob]);

  // Reset states and move to the next passage
  const handleNextPassage = () => {
    // Reset states for the next test
    setIsReading(false);
    setIsRecording(false);
    setMediaRecorder(null);
    setAudioBlob(null);
    setReadingTime(0);
    setIsTestCompleted(false);
    setReadingSpeed(0);
    setFluencyRating(null);
    setStartTime(null);

    // Move to next passage if available; otherwise, restart from the beginning
    if (currentIndex < passagesList.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      toast.info('No more passages available. Restarting.');
      setCurrentIndex(0);
    }
  };

  return (
    <div
      className="bg-gradient-to-r from-green-200 via-blue-200 to-purple-200 min-h-screen p-8 flex flex-col items-center"
      style={{ fontFamily: 'OpenDyslexic', lineHeight: '1.5' }}
    >
      <ToastContainer />
      <h2 className="text-4xl font-bold text-blue-800 mb-8 text-center">
        Gray Oral Reading Test
      </h2>

      <div className="bg-white shadow-lg rounded-lg p-8 max-w-3xl w-full mx-auto text-center">
        {currentPassage ? (
          <>
            <h3 className="text-xl font-bold mb-4">Read the following passage:</h3>
            <p className="text-gray-700 mb-4">{currentPassage}</p>
          </>
        ) : (
          <p>Loading passage...</p>
        )}

        {!isReading && !isTestCompleted && (
          <button
            onClick={handleStartReading}
            className="bg-gradient-to-r from-green-400 to-green-600 text-white px-6 py-3 rounded-full shadow-lg hover:shadow-xl transition duration-300 ease-in-out transform hover:scale-105"
          >
            Start Reading
          </button>
        )}

        {isReading && (
          <button
            onClick={handleFinishReading}
            className="bg-gradient-to-r from-red-400 to-red-600 text-white px-6 py-3 rounded-full shadow-lg hover:shadow-xl transition duration-300 ease-in-out transform hover:scale-105"
          >
            Finish Reading
          </button>
        )}

        {isTestCompleted && (
          <div className="mt-8 bg-gradient-to-r from-purple-100 to-blue-100 p-6 rounded-lg shadow-md text-left">
            <h4 className="text-lg font-semibold text-purple-800 mb-2">Results:</h4>
            <p className="text-gray-800 mb-1">
              Time Taken: <span className="font-semibold">{readingTime.toFixed(2)} seconds</span>
            </p>
            <p className="text-gray-800 mb-1">
              Reading Speed: <span className="font-semibold">{readingSpeed} words per minute</span>
            </p>
            {fluencyRating !== null && (
              <p className="text-gray-800">
                Fluency Rating: <span className="font-semibold">{fluencyRating}</span>
              </p>
            )}
            <button
              onClick={handleNextPassage}
              className="mt-4 bg-gradient-to-r from-blue-500 to-indigo-600 text-white px-6 py-3 rounded-full shadow-lg hover:shadow-xl transition duration-300 ease-in-out transform hover:scale-105"
            >
              Next Passage
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default GrayOralReadingTest;
