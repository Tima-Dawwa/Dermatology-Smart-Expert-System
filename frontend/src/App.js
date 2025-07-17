import "./App.css";
import WelcomePage from "./welcome_page";
import QuestionPage from "./question_page";
import ResultsPage from "./result_page";
import SessionReviewPage from "./session_review";
import { BackendProvider, useBackend } from "./api/BackendContext";
import { useState, useEffect } from "react";

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
          saveResults={() => {}}
          printResults={() => {}}
          resultsTextRef={null}
          showReview={handleShowReview}
        />
      )}
      {page === "session_review" && (
        <SessionReviewPage goBack={handleBackToResults}/>
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
