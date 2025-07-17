import "./App.css";
import WelcomePage from "./welcome_page";
import QuestionPage from "./question_page";
import ResultsPage from "./result_page";
import SessionReviewPage  from "./session_review";
import { BackendProvider, useBackend } from "./api/BackendContext";

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

  // Navigation logic
  let page = "welcome";
  if (sessionId && currentQuestion) page = "question";
  if (sessionId && diagnosis) page = "result";

  // Handlers
  const handleStart = () => createSession();
  const handleSubmitAnswer = (answer) => submitAnswer(answer);
  const handleReset = () => resetSession();

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
          showReview={() => {}} // here is the logic of the button , it have to navigate to review page
        />
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
