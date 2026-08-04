import { motion } from "framer-motion";

const SIZE = 320;
const CENTER = SIZE / 2;

export default function InnerRing() {
  return (
    <motion.svg
      width={SIZE}
      height={SIZE}
      viewBox={`0 0 ${SIZE} ${SIZE}`}
      className="absolute"
      animate={{ rotate: 360 }}
      transition={{
        duration: 25,
        repeat: Infinity,
        ease: "linear",
      }}
    >
      <circle
        cx={CENTER}
        cy={CENTER}
        r="120"
        fill="none"
        stroke="#36D7FF"
        strokeWidth="2"
        strokeDasharray="4 10"
        opacity="0.6"
      />
    </motion.svg>
  );
}