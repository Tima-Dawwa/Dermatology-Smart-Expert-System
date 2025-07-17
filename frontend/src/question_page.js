import { ChevronRight } from "lucide-react";

const QuestionPage = ({
  currentQuestion,
  questionIndex,
  mockQuestions,
  isProcessing,
  inputValue,
  setInputValue,
  selectedChoice,
  setSelectedChoice,
  selectedMultiple,
  handleMultipleChoice,
  submitAnswer,
}) => {
  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-br from-blue-100 via-indigo-100 to-pink-100 px-2 sm:px-4 lg:px-8 py-4 sm:py-8 lg:py-12">
      <div className="w-full max-w-3xl flex-1 flex flex-col justify-center">
        {/* Progress Header */}
        <div className="text-center mb-6 sm:mb-8">
          <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-1 sm:mb-2">
            Assessment in Progress
          </h2>
          <p className="text-gray-600 text-base sm:text-lg">
            Please answer the following questions accurately for the best results
          </p>
        </div>

        {/* Progress Bar */}
        <div className="bg-gray-50 rounded-2xl p-4 sm:p-6 mb-6 sm:mb-8 shadow-sm">
          <div className="flex items-center justify-between mb-2 sm:mb-3">
            <span className="text-sm font-semibold text-gray-700">Progress</span>
            <span className="text-sm text-gray-500">
              {questionIndex + 1} of {mockQuestions.length}
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div
              className="h-3 rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 transition-all duration-500"
              style={{
                width: `${((questionIndex + 1) / mockQuestions.length) * 100}%`,
              }}
            />
          </div>
          {isProcessing && (
            <div className="mt-3 flex items-center space-x-2 text-indigo-600">
              <div className="animate-spin rounded-full h-4 w-4 border-2 border-indigo-600 border-t-transparent"></div>
              <span className="text-sm">Processing your response...</span>
            </div>
          )}
        </div>

        {/* Question Card */}
        <div className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
          <div className="bg-gradient-to-r from-indigo-500 to-purple-600 px-6 sm:px-8 py-4 sm:py-6">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold">{questionIndex + 1}</span>
              </div>
              <h3 className="text-lg sm:text-xl font-semibold text-white">
                Assessment Question
              </h3>
            </div>
          </div>

          <div className="p-5 sm:p-8">
            {/* Question Text */}
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-4 sm:p-6 rounded-xl mb-6 sm:mb-8 border border-blue-100">
              <p className="text-base sm:text-lg text-gray-800 leading-relaxed">
                {currentQuestion?.text}
              </p>
            </div>

            {/* Answer Options */}
            <div className="space-y-5 sm:space-y-6">
              {currentQuestion?.type === "number" ? (
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Please enter a numerical value:
                  </label>
                  <input
                    type="number"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    className="w-full px-5 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-base sm:text-lg"
                    placeholder="Enter number..."
                  />
                </div>
              ) : (
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-3">
                    {currentQuestion?.allowMultiple
                      ? "Select all that apply:"
                      : "Select your answer:"}
                  </label>
                  <div className="grid gap-2 sm:gap-3">
                    {currentQuestion?.options?.map((option, index) => (
                      <div
                        key={index}
                        className={`p-3 sm:p-4 rounded-xl border-2 transition-all cursor-pointer hover:bg-gray-50 ${
                          currentQuestion.allowMultiple
                            ? selectedMultiple.includes(option)
                              ? "border-indigo-500 bg-indigo-50"
                              : "border-gray-200"
                            : selectedChoice === option
                            ? "border-indigo-500 bg-indigo-50"
                            : "border-gray-200"
                        }`}
                        onClick={() => {
                          if (currentQuestion.allowMultiple) {
                            handleMultipleChoice(option);
                          } else {
                            setSelectedChoice(option);
                          }
                        }}
                      >
                        <div className="flex items-center space-x-3">
                          {currentQuestion.allowMultiple ? (
                            <input
                              type="checkbox"
                              checked={selectedMultiple.includes(option)}
                              onChange={() => handleMultipleChoice(option)}
                              className="w-5 h-5 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                            />
                          ) : (
                            <input
                              type="radio"
                              name="question-option"
                              value={option}
                              checked={selectedChoice === option}
                              onChange={(e) => setSelectedChoice(e.target.value)}
                              className="w-5 h-5 text-indigo-600 border-gray-300 focus:ring-indigo-500"
                            />
                          )}
                          <label className="text-base font-medium text-gray-800 cursor-pointer">
                            {option}
                          </label>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="pt-2 sm:pt-4">
                <button
                  onClick={submitAnswer}
                  disabled={isProcessing}
                  className="w-full flex items-center justify-center space-x-3 px-8 py-3 sm:py-4 bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-semibold rounded-xl hover:from-indigo-600 hover:to-purple-700 transition-all transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none text-base sm:text-lg"
                >
                  <span>Submit Answer</span>
                  <ChevronRight className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuestionPage;
