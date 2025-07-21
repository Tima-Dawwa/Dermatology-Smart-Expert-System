import "./App.css";
import WelcomePage from "./welcome_page";
import QuestionPage from "./question_page";
import ResultsPage from "./result_page";
import SessionReviewPage from "./session_review";
import { BackendProvider, useBackend } from "./api/BackendContext";
import { useState, useEffect, useRef } from "react";

function MainApp() {
  const {
    sessionId,
    currentQuestion,
    diagnosis,
    loading,
    createSession,
    submitAnswer,
    resetSession,
  } = useBackend();

  const [page, setPage] = useState("welcome");
  const resultsTextRef = useRef(null);

  useEffect(() => {
    if (!sessionId) {
      setPage("welcome");
    } else if (diagnosis) {
      setPage("result");
    } else if (currentQuestion) {
      setPage("question");
    }
  }, [sessionId, diagnosis, currentQuestion]);

  const handleStart = () => createSession();
  const handleSubmitAnswer = (answer) => submitAnswer(answer);
  const handleReset = () => {
    resetSession();
    setPage("welcome");
  };
  const handleShowReview = () => {
    setPage("session_review");
  };
  const handleBackToResults = () => {
    setPage("result");
  };

  // --- Save Results Implementation ---
  const handleSaveResults = () => {
    const text = diagnosis?.explanation || "";
    const blob = new Blob([text], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "dermatology_diagnosis.txt";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // --- Print Results Implementation ---
  const handlePrintResults = () => {
    if (resultsTextRef.current) {
      const printWindow = window.open("", "_blank");
      printWindow.document.write(`
        <html>
          <head>
            <title>Diagnosis Results</title>
            <style>
              body { font-family: Arial, sans-serif; margin: 40px; }
              .content { white-space: pre-wrap; font-family: monospace; font-size: 1rem; }
            </style>
          </head>
          <body>
            <h2>Dermatology Diagnosis Results</h2>
            <div class="content">${resultsTextRef.current.innerText}</div>
          </body>
        </html>
      `);
      printWindow.document.close();
      printWindow.focus();
      printWindow.print();
    }
  };

  return (
    <div className="App">
      {page === "welcome" && (
        <WelcomePage startDiagnosis={handleStart} isProcessing={loading} />
      )}
      {page === "question" && (
        <QuestionPage
          currentQuestion={currentQuestion}
          isProcessing={loading}
          submitAnswer={handleSubmitAnswer}
        />
      )}
      {page === "result" && (
        <ResultsPage
          results={diagnosis?.explanation || ""}
          resetDiagnosis={handleReset}
          saveResults={handleSaveResults}
          printResults={handlePrintResults}
          resultsTextRef={resultsTextRef}
          showReview={handleShowReview}
        />
      )}
      {page === "session_review" && (
        <SessionReviewPage goBack={handleBackToResults} />
      )}
    </div>
  );
}

function App() {
  return (
    <BackendProvider>
      <MainApp />
    </BackendProvider>
  );
}

export default App;
