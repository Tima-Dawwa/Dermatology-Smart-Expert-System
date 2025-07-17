import { CheckCircle, FileText, RotateCcw, Save, Printer } from "lucide-react";

const ResultsPage = ({
  results,
  resetDiagnosis,
  saveResults,
  printResults,
  resultsTextRef,
}) => {
  return (
    <div className="max-w-5xl mx-auto">
      {/* Results Header */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center space-x-2 bg-emerald-100 text-emerald-800 px-4 py-2 rounded-full text-sm font-medium mb-4">
          <CheckCircle className="w-4 h-4" />
          <span>Assessment Complete</span>
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          Your Diagnosis Results
        </h2>
        <p className="text-gray-600">
          Based on your responses, here's our comprehensive analysis
        </p>
      </div>

      {/* Results Card */}
      <div className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden mb-8">
        <div className="bg-gradient-to-r from-emerald-500 to-green-600 px-8 py-6">
          <div className="flex items-center space-x-3">
            <FileText className="w-8 h-8 text-white" />
            <h3 className="text-xl font-semibold text-white">
              Detailed Analysis Report
            </h3>
          </div>
        </div>

        <div className="p-8">
          <div
            className="bg-gray-50 rounded-xl p-6 max-h-96 overflow-y-auto font-mono text-sm leading-relaxed whitespace-pre-wrap"
            ref={resultsTextRef}
          >
            {results}
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-wrap gap-4 justify-center">
        <button
          onClick={resetDiagnosis}
          className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-semibold rounded-xl hover:from-indigo-600 hover:to-purple-700 transition-all transform hover:scale-105"
        >
          <RotateCcw className="w-5 h-5" />
          <span>Start New Assessment</span>
        </button>

        <button
          onClick={saveResults}
          className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-emerald-500 to-green-600 text-white font-semibold rounded-xl hover:from-emerald-600 hover:to-green-700 transition-all transform hover:scale-105"
        >
          <Save className="w-5 h-5" />
          <span>Save Results</span>
        </button>

        <button
          onClick={printResults}
          className="flex items-center space-x-2 px-6 py-3 bg-white border-2 border-gray-300 text-gray-700 font-semibold rounded-xl hover:bg-gray-50 hover:border-gray-400 transition-all transform hover:scale-105"
        >
          <Printer className="w-5 h-5" />
          <span>Print Results</span>
        </button>
      </div>
    </div>
  );
};

export default ResultsPage;
