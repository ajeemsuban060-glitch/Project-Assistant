import { motion } from "framer-motion";

export default function AnimatedBackground() {
  return (
    <div className="absolute inset-0 overflow-hidden -z-10">

      {/* Base Background */}
      <div className="absolute inset-0 bg-[#030712]" />

      {/* Cyan Glow */}
      <motion.div
        animate={{
          x: [0, 80, 0],
          y: [0, -60, 0],
          scale: [1, 1.2, 1],
        }}
        transition={{
          duration: 18,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="
          absolute
          -top-32
          left-1/4
          h-[500px]
          w-[500px]
          rounded-full
          bg-cyan-400/20
          blur-[140px]
        "
      />

      {/* Violet Glow */}
      <motion.div
        animate={{
          x: [0, -120, 0],
          y: [0, 80, 0],
          scale: [1.1, 0.9, 1.1],
        }}
        transition={{
          duration: 22,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="
          absolute
          bottom-[-180px]
          right-[-120px]
          h-[600px]
          w-[600px]
          rounded-full
          bg-violet-500/15
          blur-[180px]
        "
      />

      {/* Center Glow */}
      <motion.div
        animate={{
          opacity: [0.15, 0.3, 0.15],
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
        }}
        className="
          absolute
          left-1/2
          top-1/2
          h-[420px]
          w-[420px]
          -translate-x-1/2
          -translate-y-1/2
          rounded-full
          bg-cyan-300/10
          blur-[120px]
        "
      />

    </div>
  );
}