import React from "react";
import { useBackend } from "./api/BackendContext";
import { ArrowLeft } from "lucide-react";

const SessionReviewPage = ({ goBack }) => {
  const { answers, diagnosis } = useBackend();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 py-10 px-4 sm:px-10">
      <div className="max-w-4xl mx-auto bg-white rounded-2xl shadow-lg p-6 sm:p-10 border border-gray-200 text-left">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800">🧾 Session Review</h2>
          <button
            onClick={goBack}
            className="flex items-center space-x-2 text-sm text-blue-600 hover:text-blue-800 transition"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Results</span>
          </button>
        </div>

        {diagnosis && (
          <div className="bg-green-100 border-l-4 border-green-400 p-4 rounded mb-6">
            <h3 className="text-lg font-semibold text-green-800">
              Final Diagnosis: {diagnosis.disease}
            </h3>
            {(() => {
      const reasoning = diagnosis.reasoning || "";
      const lines = reasoning.split(";");
      const firstLine = lines[0];
      const penaltyLines = lines.slice(1);

      return (
        <div className="text-sm text-green-700 space-y-1 mt-1">
          <div><strong>Confidence:</strong> {(diagnosis.confidence).toFixed(2)}%</div>
          <div> {firstLine.trim()}</div>
          {penaltyLines.map((line, i) => (
            <div key={i}> {line.trim()}</div>
          ))}
        </div>
      );
    })()}
            
          </div>
        )}
        <div className="space-y-5">
          {answers.length > 0 ? (
            answers.map((entry, index) => (
              <div key={index} className="border-l-4 border-blue-500 pl-4">
                <p className="font-semibold text-gray-900">
                  {index + 1}. {entry.question.question_text }
                </p>
                <p className="text-sm text-gray-600">
                  Your Answer:{" "}
                  {Array.isArray(entry.answer)
                    ? entry.answer.join(", ")
                    : entry.answer}
                </p>
              </div>
            ))
          ) : (
            <p className="text-gray-500">No session data available.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default SessionReviewPage;
