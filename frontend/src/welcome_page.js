import { Star, Brain, Shield, Users, ChevronRight } from "lucide-react";
import { motion } from "framer-motion";

const featureVariants = {
  hidden: { opacity: 0, y: 40 },
  visible: (i) => ({
    opacity: 1,
    y: 0,
    transition: {
      delay: i * 0.18 + 0.2,
      duration: 0.7,
      type: "spring",
      stiffness: 60,
    },
  }),
};

const WelcomePage = ({ startDiagnosis, isProcessing }) => {
  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-br from-white to-blue-50 px-2 sm:px-6 lg:px-8">
      <div className="w-full max-w-7xl flex-1 flex flex-col justify-center">
        {/* Hero Section */}
        <div className="text-center mb-8 sm:mb-12 lg:mb-16">
          <div className="inline-flex items-center space-x-2 bg-indigo-100 text-indigo-800 px-4 py-2 sm:px-6 sm:py-3 rounded-full text-sm sm:text-base font-medium mb-4 sm:mb-6">
            <Star className="w-4 h-4 sm:w-5 sm:h-5" />
            <span>Advanced AI Technology</span>
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl xl:text-6xl font-bold text-gray-900 mb-4 sm:mb-6 px-2 leading-tight">
            Welcome to Your Personal Dermatology Assistant
          </h2>
          <p className="text-lg sm:text-xl lg:text-2xl text-gray-600 max-w-3xl mx-auto leading-relaxed px-2">
            Our state-of-the-art AI system provides comprehensive skin condition analysis through an intelligent assessment process. Get professional-grade insights in minutes.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6 lg:gap-8 mb-8 sm:mb-12 lg:mb-16">
          {[{
            icon: <Brain className="w-7 h-7 sm:w-8 sm:h-8 text-white" />, bg: "bg-blue-500", title: "AI-Powered Analysis", desc: "Advanced machine learning algorithms analyze your symptoms with medical precision.", gradient: "from-blue-50 to-indigo-50 border-blue-100"
          }, {
            icon: <Shield className="w-7 h-7 sm:w-8 sm:h-8 text-white" />, bg: "bg-emerald-500", title: "Secure & Private", desc: "Your health information is protected with enterprise-grade security measures.", gradient: "from-emerald-50 to-green-50 border-emerald-100"
          }, {
            icon: <Users className="w-7 h-7 sm:w-8 sm:h-8 text-white" />, bg: "bg-purple-500", title: "Expert Insights", desc: "Backed by dermatological expertise and clinical research data.", gradient: "from-purple-50 to-pink-50 border-purple-100"
          }].map((f, i) => (
            <motion.div
              key={f.title}
              className={`bg-gradient-to-br ${f.gradient} p-5 sm:p-7 lg:p-8 rounded-2xl border flex flex-col items-center text-center shadow-sm`}
              custom={i}
              initial="hidden"
              animate="visible"
              variants={featureVariants}
              whileHover={{ scale: 1.08 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              <div className={`w-12 h-12 sm:w-14 sm:h-14 ${f.bg} rounded-2xl flex items-center justify-center mb-4`}>
                {f.icon}
              </div>
              <h3 className="text-lg sm:text-xl font-semibold text-gray-900 mb-2">{f.title}</h3>
              <p className="text-base sm:text-lg text-gray-600 leading-relaxed">{f.desc}</p>
            </motion.div>
          ))}
        </div>

        {/* CTA Section */}
        <div className="text-center">
          <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-6 sm:p-10 lg:p-12 rounded-2xl text-white mb-4 sm:mb-8 shadow-xl flex flex-col items-center">
            <h3 className="text-xl sm:text-2xl lg:text-3xl font-bold mb-4 sm:mb-6 px-2">
              Ready to Begin Your Assessment?
            </h3>
            <p className="text-indigo-100 mb-6 sm:mb-8 max-w-2xl mx-auto text-base sm:text-lg px-2 leading-relaxed">
              Answer a few simple questions about your skin condition and receive a comprehensive analysis with personalized recommendations.
            </p>
            <button
              onClick={startDiagnosis}
              disabled={isProcessing}
              className="inline-flex items-center space-x-3 px-8 sm:px-12 py-4 sm:py-5 bg-white text-indigo-600 font-bold rounded-2xl hover:bg-gray-50 transition-all transform hover:scale-105 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed text-lg sm:text-xl"
            >
              <span className="text-2xl sm:text-3xl">🚀</span>
              <span>Begin Assessment</span>
              <ChevronRight className="w-6 h-6 sm:w-7 sm:h-7" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WelcomePage;
