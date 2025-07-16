import React, { useState,  useRef } from "react";
import {
  Activity,
  AlertCircle,
  CheckCircle,
  FileText,
  Printer,
  RotateCcw,
  Save,
  Stethoscope,
  ChevronRight,
  Star,
  Shield,
  Brain,
  Users,
} from "lucide-react";

const DermatologyExpertSystem = () => {
  const [currentView, setCurrentView] = useState("welcome");
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [status, setStatus] = useState({ message: "Ready", type: "success" });
  const [results, setResults] = useState("");
  const [inputValue, setInputValue] = useState("");
  const [selectedChoice, setSelectedChoice] = useState("");
  const [selectedMultiple, setSelectedMultiple] = useState([]);
  const resultsTextRef = useRef(null);

  const mockQuestions = [
    {
      id: 1,
      text: "What is the duration of your skin condition?",
      type: "choice",
      options: [
        "Less than 1 week",
        "1-2 weeks",
        "2-4 weeks",
        "1-3 months",
        "More than 3 months",
      ],
      allowMultiple: false,
    },
    {
      id: 2,
      text: "Please select all locations where you notice symptoms:",
      type: "choice",
      options: [
        "Face",
        "Arms",
        "Legs",
        "Torso",
        "Hands",
        "Feet",
        "Scalp",
        "Neck",
      ],
      allowMultiple: true,
    },
    {
      id: 3,
      text: "How would you rate the severity of your symptoms?",
      type: "choice",
      options: ["Mild", "Moderate", "Severe", "Very Severe"],
      allowMultiple: false,
    },
    {
      id: 4,
      text: "What is your age?",
      type: "number",
      options: [],
    },
  ];

  const [questionIndex, setQuestionIndex] = useState(0);

  const updateStatus = (message, type = "info") => {
    setStatus({ message, type });
  };

  const startDiagnosis = () => {
    updateStatus("Assessment in progress...", "info");
    setIsProcessing(true);
    setCurrentView("question");
    setCurrentQuestion(mockQuestions[0]);
    setQuestionIndex(0);

    setTimeout(() => {
      setIsProcessing(false);
    }, 1500);
  };

  const submitAnswer = () => {
    if (!currentQuestion) return;

    let answer = "";
    if (currentQuestion.type === "number") {
      if (!inputValue.trim() || isNaN(inputValue)) {
        alert("Please enter a valid number.");
        return;
      }
      answer = inputValue;
    } else if (currentQuestion.allowMultiple) {
      if (selectedMultiple.length === 0) {
        alert("Please select at least one option.");
        return;
      }
      answer = selectedMultiple.join(", ");
    } else {
      if (!selectedChoice) {
        alert("Please select an option.");
        return;
      }
      answer = selectedChoice;
    }

    updateStatus("Processing answer...", "info");
    setIsProcessing(true);

    setTimeout(() => {
      if (questionIndex < mockQuestions.length - 1) {
        const nextIndex = questionIndex + 1;
        setQuestionIndex(nextIndex);
        setCurrentQuestion(mockQuestions[nextIndex]);
        setInputValue("");
        setSelectedChoice("");
        setSelectedMultiple([]);
        setIsProcessing(false);
      } else {
        completeDiagnosis();
      }
    }, 2000);
  };

  const completeDiagnosis = () => {
    const mockResults = `🏥 DIAGNOSIS RESULTS
${"=".repeat(50)}

📋 Primary Diagnosis: Atopic Dermatitis
    Confidence: 85.2%
    Reasoning: Based on the duration, location, and severity of symptoms, the pattern strongly suggests atopic dermatitis. The chronic nature and distribution are consistent with this condition.

🤖 AI Explanation:
Atopic dermatitis, commonly known as eczema, is a chronic inflammatory skin condition characterized by itchy, red, and inflamed skin. The diagnosis is based on your reported symptoms including the duration of more than 3 months, involvement of multiple body areas, and moderate to severe intensity. This condition often has a genetic component and can be triggered by environmental factors such as allergens, stress, or weather changes.

Treatment typically involves:
• Moisturizing regularly with fragrance-free products
• Using topical corticosteroids during flare-ups
• Avoiding known triggers
• Maintaining good skin hygiene

Please consult with a dermatologist for proper evaluation and personalized treatment plan.`;

    setResults(mockResults);
    setCurrentView("results");
    updateStatus("Assessment complete", "success");
    setIsProcessing(false);
  };

  const resetDiagnosis = () => {
    setCurrentView("welcome");
    setCurrentQuestion(null);
    setQuestionIndex(0);
    setIsProcessing(false);
    setResults("");
    setInputValue("");
    setSelectedChoice("");
    setSelectedMultiple([]);
    updateStatus("Ready", "success");
  };

  const handleMultipleChoice = (option) => {
    setSelectedMultiple((prev) =>
      prev.includes(option)
        ? prev.filter((item) => item !== option)
        : [...prev, option]
    );
  };

  const saveResults = () => {
    const element = document.createElement("a");
    const file = new Blob([results], { type: "text/plain" });
    element.href = URL.createObjectURL(file);
    element.download = `diagnosis_results_${
      new Date().toISOString().split("T")[0]
    }.txt`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const printResults = () => {
    const printWindow = window.open("", "_blank");
    printWindow.document.write(`
      <!DOCTYPE html>
      <html>
      <head>
        <title>Dermatology Diagnosis Report</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
          .header { text-align: center; border-bottom: 2px solid #2C3E50; padding-bottom: 20px; margin-bottom: 30px; }
          .content { white-space: pre-wrap; }
          .disclaimer { background-color: #f8f9fa; padding: 15px; border-left: 4px solid #F39C12; margin-top: 30px; }
          @media print { body { margin: 20px; } }
        </style>
      </head>
      <body>
        <div class="header">
          <h1>Dermatology Expert System</h1>
          <h2>Diagnosis Report</h2>
          <p>Generated on: ${new Date().toLocaleString()}</p>
        </div>
        <div class="content">${results}</div>
        <div class="disclaimer">
          <strong>DISCLAIMER:</strong> This report is generated by an AI-based expert system
          and should not replace professional medical consultation. Always consult qualified
          healthcare professionals for proper diagnosis and treatment.
        </div>
      </body>
      </html>
    `);
    printWindow.document.close();
    printWindow.print();
  };

  const StatusIcon = () => {
    switch (status.type) {
      case "success":
        return <CheckCircle className="w-4 h-4" />;
      case "warning":
        return <AlertCircle className="w-4 h-4" />;
      case "danger":
        return <AlertCircle className="w-4 h-4" />;
      case "info":
        return <Activity className="w-4 h-4" />;
      default:
        return <Activity className="w-4 h-4" />;
    }
  };

  const getStatusColor = () => {
    switch (status.type) {
      case "success":
        return "bg-emerald-500";
      case "warning":
        return "bg-amber-500";
      case "danger":
        return "bg-red-500";
      case "info":
        return "bg-blue-500";
      default:
        return "bg-gray-500";
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <div className="max-w-7xl mx-auto p-6">
        {/* Main Content */}
        <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white/20 overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-indigo-600 via-purple-600 to-blue-600 px-8 py-8">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-6">
                <div className="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center">
                  <Stethoscope className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h1 className="text-3xl font-bold text-white mb-2">
                    Dermatology Expert System
                  </h1>
                  <p className="text-indigo-100 text-lg">
                    Advanced AI-Powered Skin Condition Analysis
                  </p>
                </div>
              </div>

              {/* Status Indicator */}
              <div
                className={`flex items-center space-x-3 px-6 py-3 rounded-2xl text-white font-semibold ${getStatusColor()} bg-opacity-90 backdrop-blur-sm`}
              >
                <StatusIcon />
                <span className="text-sm">{status.message}</span>
              </div>
            </div>
          </div>

          {/* Content Area */}
          <div className="p-8">
            {/* Welcome View */}
            {currentView === "welcome" && (
              <div className="max-w-5xl mx-auto">
                {/* Hero Section */}
                <div className="text-center mb-12">
                  <div className="inline-flex items-center space-x-2 bg-indigo-100 text-indigo-800 px-4 py-2 rounded-full text-sm font-medium mb-6">
                    <Star className="w-4 h-4" />
                    <span>Advanced AI Technology</span>
                  </div>
                  <h2 className="text-4xl font-bold text-gray-900 mb-4">
                    Welcome to Your Personal Dermatology Assistant
                  </h2>
                  <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
                    Our state-of-the-art AI system provides comprehensive skin
                    condition analysis through an intelligent assessment
                    process. Get professional-grade insights in minutes.
                  </p>
                </div>

                {/* Features Grid */}
                <div className="grid md:grid-cols-3 gap-8 mb-12">
                  <div className="bg-gradient-to-br from-blue-50 to-indigo-50 p-6 rounded-2xl border border-blue-100">
                    <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center mb-4">
                      <Brain className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      AI-Powered Analysis
                    </h3>
                    <p className="text-gray-600">
                      Advanced machine learning algorithms analyze your symptoms
                      with medical precision.
                    </p>
                  </div>

                  <div className="bg-gradient-to-br from-emerald-50 to-green-50 p-6 rounded-2xl border border-emerald-100">
                    <div className="w-12 h-12 bg-emerald-500 rounded-xl flex items-center justify-center mb-4">
                      <Shield className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      Secure & Private
                    </h3>
                    <p className="text-gray-600">
                      Your health information is protected with enterprise-grade
                      security measures.
                    </p>
                  </div>

                  <div className="bg-gradient-to-br from-purple-50 to-pink-50 p-6 rounded-2xl border border-purple-100">
                    <div className="w-12 h-12 bg-purple-500 rounded-xl flex items-center justify-center mb-4">
                      <Users className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      Expert Insights
                    </h3>
                    <p className="text-gray-600">
                      Backed by dermatological expertise and clinical research
                      data.
                    </p>
                  </div>
                </div>

                {/* CTA Section */}
                <div className="text-center">
                  <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-8 rounded-2xl text-white mb-8">
                    <h3 className="text-2xl font-bold mb-4">
                      Ready to Begin Your Assessment?
                    </h3>
                    <p className="text-indigo-100 mb-6 max-w-2xl mx-auto">
                      Answer a few simple questions about your skin condition
                      and receive a comprehensive analysis with personalized
                      recommendations.
                    </p>
                    <button
                      onClick={startDiagnosis}
                      disabled={isProcessing}
                      className="inline-flex items-center space-x-3 px-8 py-4 bg-white text-indigo-600 font-bold rounded-2xl hover:bg-gray-50 transition-all transform hover:scale-105 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <span className="text-2xl">🚀</span>
                      <span>Begin Assessment</span>
                      <ChevronRight className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Question View */}
            {currentView === "question" && (
              <div className="max-w-4xl mx-auto space-y-8">
                {/* Progress Header */}
                <div className="text-center mb-8">
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">
                    Assessment in Progress
                  </h2>
                  <p className="text-gray-600">
                    Please answer the following questions accurately for the
                    best results
                  </p>
                </div>

                {/* Progress Bar */}
                <div className="bg-gray-50 rounded-2xl p-6 mb-8">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-sm font-semibold text-gray-700">
                      Progress
                    </span>
                    <span className="text-sm text-gray-500">
                      {questionIndex + 1} of {mockQuestions.length}
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className="h-3 rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 transition-all duration-500"
                      style={{
                        width: `${
                          ((questionIndex + 1) / mockQuestions.length) * 100
                        }%`,
                      }}
                    />
                  </div>
                  {isProcessing && (
                    <div className="mt-4 flex items-center space-x-2 text-indigo-600">
                      <div className="animate-spin rounded-full h-4 w-4 border-2 border-indigo-600 border-t-transparent"></div>
                      <span className="text-sm">
                        Processing your response...
                      </span>
                    </div>
                  )}
                </div>

                {/* Question Card */}
                <div className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
                  <div className="bg-gradient-to-r from-indigo-500 to-purple-600 px-8 py-6">
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center">
                        <span className="text-white font-bold">
                          {questionIndex + 1}
                        </span>
                      </div>
                      <h3 className="text-xl font-semibold text-white">
                        Assessment Question
                      </h3>
                    </div>
                  </div>

                  <div className="p-8">
                    {/* Question Text */}
                    <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-xl mb-8 border border-blue-100">
                      <p className="text-lg text-gray-800 leading-relaxed">
                        {currentQuestion?.text}
                      </p>
                    </div>

                    {/* Answer Options */}
                    <div className="space-y-6">
                      {currentQuestion?.type === "number" ? (
                        <div>
                          <label className="block text-sm font-semibold text-gray-700 mb-3">
                            Please enter a numerical value:
                          </label>
                          <input
                            type="number"
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            className="w-full px-6 py-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-lg"
                            placeholder="Enter number..."
                          />
                        </div>
                      ) : (
                        <div>
                          <label className="block text-sm font-semibold text-gray-700 mb-4">
                            {currentQuestion?.allowMultiple
                              ? "Select all that apply:"
                              : "Select your answer:"}
                          </label>
                          <div className="grid gap-3">
                            {currentQuestion?.options?.map((option, index) => (
                              <div
                                key={index}
                                className={`p-4 rounded-xl border-2 transition-all cursor-pointer hover:bg-gray-50 ${
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
                                      checked={selectedMultiple.includes(
                                        option
                                      )}
                                      onChange={() =>
                                        handleMultipleChoice(option)
                                      }
                                      className="w-5 h-5 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                                    />
                                  ) : (
                                    <input
                                      type="radio"
                                      name="question-option"
                                      value={option}
                                      checked={selectedChoice === option}
                                      onChange={(e) =>
                                        setSelectedChoice(e.target.value)
                                      }
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

                      <div className="pt-4">
                        <button
                          onClick={submitAnswer}
                          disabled={isProcessing}
                          className="w-full flex items-center justify-center space-x-3 px-8 py-4 bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-semibold rounded-xl hover:from-indigo-600 hover:to-purple-700 transition-all transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                        >
                          <span>Submit Answer</span>
                          <ChevronRight className="w-5 h-5" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Results View */}
            {currentView === "results" && (
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
            )}
          </div>

          {/* Footer */}
          <div className="bg-gray-50 px-8 py-6 border-t border-gray-100">
            <div className="flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0">
              <div className="flex items-center space-x-3 bg-amber-100 text-amber-800 px-4 py-2 rounded-xl">
                <AlertCircle className="w-5 h-5" />
                <span className="text-sm font-medium">
                  Medical Disclaimer: For assessment purposes only - Always
                  consult healthcare professionals
                </span>
              </div>
              <div className="text-sm text-gray-500 font-medium">
                Dermatology Expert System v2.0.0 | Professional Edition
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DermatologyExpertSystem;
