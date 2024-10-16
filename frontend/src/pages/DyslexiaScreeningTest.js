import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { FaCheckCircle } from 'react-icons/fa'; // Tick mark icon

const tests = [
  {
    title: 'Phonological Awareness Test',
    description: 'A test designed to evaluate the ability to recognize and manipulate the sounds of spoken language.',
  },
  {
    title: 'Kauffman Assessment Battery Test',
    description: 'A comprehensive assessment used to evaluate memory and cognitive abilities, helping identify learning differences.',
    link: '/kauffman-memory-test',
    localStorageKey: 'kauffmanTestCompleted', // Key for tracking completion
  },
  {
    title: 'Gray Oral Reading Test',
    description: 'A standardized test used to measure reading fluency and comprehension skills in individuals.',
    link:'/gray-oral-reading'
  },
];

const DyslexiaScreeningTestsPage = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [completedTests, setCompletedTests] = useState({});

  useEffect(() => {
    setIsVisible(true);

    // Check for completed tests
    const completionStatus = {};
    tests.forEach(test => {
      if (test.localStorageKey) {
        const isCompleted = localStorage.getItem(test.localStorageKey) === 'true';
        if (isCompleted) {
          completionStatus[test.title] = true;
        }
      }
    });
    setCompletedTests(completionStatus);
  }, []);

  return (
    <section className="bg-gradient-to-r from-green-200 via-blue-200 to-purple-200 min-h-screen p-8">
      <h2 className="text-2xl font-semibold text-blue-700 mb-4">Dyslexia Screening Tests</h2>
      <div className="grid grid-cols-1 gap-6">
        {tests.map((test, index) => (
          <div
            key={index}
            className={`bg-white p-6 rounded-lg shadow-md transform transition-all duration-700 ease-out
              ${isVisible ? `animate-crazyCardAnimation delay-${index * 200}` : 'opacity-0'}`}
          >
            <div className="flex justify-between items-center">
              <h3 className="text-xl font-bold text-blue-700 mb-2">
                {test.link ? (
                  <Link to={test.link} className="hover:underline">
                    {test.title}
                  </Link>
                ) : (
                  test.title
                )}
              </h3>
              {completedTests[test.title] && (
                <FaCheckCircle
                  className="text-green-500 text-4xl transition-transform transform hover:scale-110"
                  style={{ filter: 'drop-shadow(0px 4px 6px rgba(0, 128, 0, 0.4))' }}
                />
              )}
            </div>
            <p className="text-gray-600">{test.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default DyslexiaScreeningTestsPage;