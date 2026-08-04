import { motion } from "framer-motion";

export default function PulseRing() {
  return (
    <motion.div
      animate={{
        scale: [1, 1.08, 1],
        opacity: [0.15, 0.35, 0.15],
      }}
      transition={{
        duration: 2.5,
        repeat: Infinity,
      }}
      className="
      absolute
      h-[320px]
      w-[320px]
      rounded-full
      border
      border-cyan-400/30
    "
    />
  );
}