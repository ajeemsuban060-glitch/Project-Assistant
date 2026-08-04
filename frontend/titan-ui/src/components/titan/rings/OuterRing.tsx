import { motion } from "framer-motion";

export default function OuterRing() {
  return (
    <motion.div
      animate={{
        rotate: 360,
      }}
      transition={{
        duration: 80,
        repeat: Infinity,
        ease: "linear",
      }}
      className="
        absolute
        h-[340px]
        w-[340px]
        rounded-full
        border
        border-cyan-400/20
      "
    />
  );
}