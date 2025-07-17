import React, { useState, useRef } from "react";
import "./App.css";
import WelcomePage from "./welcome_page";
import QuestionPage from "./question_page";
import ResultsPage from "./result_page";

// Mock questions for demonstration
const mockQuestions = [
  {
    text: "What is the main symptom you are experiencing?",
    type: "single",
    options: ["Rash", "Itching", "Redness", "Swelling"],
    allowMultiple: false,
  },
  {
    text: "Select all affected areas:",
    type: "multi",
    options: ["Face", "Arms", "Legs", "Torso"],
    allowMultiple: true,
  },
  {
    text: "How many days have you had these symptoms?",
    type: "number",
    allowMultiple: false,
  },
];

function App() {
  const [page, setPage] = useState("welcome");
  const [isProcessing, setIsProcessing] = useState(false);
  const [questionIndex, setQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [selectedChoice, setSelectedChoice] = useState("");
  const [selectedMultiple, setSelectedMultiple] = useState([]);
  const resultsTextRef = useRef(null);

  // Handler to start diagnosis
  const startDiagnosis = () => {
    setAnswers([]);
    setQuestionIndex(0);
    setInputValue("");
    setSelectedChoice("");
    setSelectedMultiple([]);
    setPage("question");
  };

  // Handler for multiple choice selection
  const handleMultipleChoice = (option) => {
    setSelectedMultiple((prev) =>
      prev.includes(option)
        ? prev.filter((o) => o !== option)
        : [...prev, option]
    );
  };

  // Handler to submit answer
  const submitAnswer = () => {
    setIsProcessing(true);
    setTimeout(() => {
      let answer;
      const current = mockQuestions[questionIndex];
      if (current.type === "number") {
        answer = inputValue;
      } else if (current.allowMultiple) {
        answer = selectedMultiple;
      } else {
        answer = selectedChoice;
      }
      setAnswers((prev) => [...prev, answer]);
      setInputValue("");
      setSelectedChoice("");
      setSelectedMultiple([]);
      if (questionIndex + 1 < mockQuestions.length) {
        setQuestionIndex((idx) => idx + 1);
      } else {
        setPage("result");
      }
      setIsProcessing(false);
    }, 500); // Simulate processing
  };

  // Handler to reset diagnosis
  const resetDiagnosis = () => {
    setPage("welcome");
    setAnswers([]);
    setQuestionIndex(0);
    setInputValue("");
    setSelectedChoice("");
    setSelectedMultiple([]);
  };

  // Handler to save results (placeholder)
  const saveResults = () => {
    alert("Results saved (placeholder)");
  };

  // Handler to print results (placeholder)
  const printResults = () => {
    alert("Print dialog opened (placeholder)");
  };

  // Generate mock results text
  const results =
    "Diagnosis: Example Skin Condition\n" +
    "Confidence: 92%\n" +
    "Reasoning: Based on your answers: " + JSON.stringify(answers, null, 2);

  return (
    <div className="App">
      {page === "welcome" && (
        <WelcomePage startDiagnosis={startDiagnosis} isProcessing={isProcessing} />
      )}
      {page === "question" && (
        <QuestionPage
          currentQuestion={mockQuestions[questionIndex]}
          questionIndex={questionIndex}
          mockQuestions={mockQuestions}
          isProcessing={isProcessing}
          inputValue={inputValue}
          setInputValue={setInputValue}
          selectedChoice={selectedChoice}
          setSelectedChoice={setSelectedChoice}
          selectedMultiple={selectedMultiple}
          handleMultipleChoice={handleMultipleChoice}
          submitAnswer={submitAnswer}
        />
      )}
      {page === "result" && (
        <ResultsPage
          results={results}
          resetDiagnosis={resetDiagnosis}
          saveResults={saveResults}
          printResults={printResults}
          resultsTextRef={resultsTextRef}
        />
      )}
    </div>
  );
}

export default App;
