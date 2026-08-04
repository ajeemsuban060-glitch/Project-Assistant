import { motion } from "framer-motion";

export default function GlowLayer() {
  return (
    <>
      {/* Cyan Glow */}
      <motion.div
        animate={{
          scale: [1, 1.08, 1],
          opacity: [0.18, 0.28, 0.18],
        }}
        transition={{
          duration: 4,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="
          absolute
          h-[420px]
          w-[420px]
          rounded-full
          bg-cyan-400/20
          blur-[120px]
        "
      />

      {/* Violet Glow */}
      <motion.div
        animate={{
          scale: [1.1, 1, 1.1],
          opacity: [0.12, 0.22, 0.12],
        }}
        transition={{
          duration: 5,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="
          absolute
          h-[500px]
          w-[500px]
          rounded-full
          bg-violet-500/10
          blur-[180px]
        "
      />
    </>
  );
}