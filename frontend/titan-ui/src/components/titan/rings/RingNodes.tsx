import { motion } from "framer-motion";

const SIZE = 440;
const CENTER = SIZE / 2;

const nodes = [
  { angle: 0, r: 182, size: 5 },
  { angle: 45, r: 176, size: 4 },
  { angle: 90, r: 182, size: 5 },
  { angle: 135, r: 176, size: 4 },
  { angle: 180, r: 182, size: 5 },
  { angle: 225, r: 176, size: 4 },
  { angle: 270, r: 182, size: 5 },
  { angle: 315, r: 176, size: 4 },
];

export default function RingNodes() {
  return (
    <motion.svg
      width={SIZE}
      height={SIZE}
      viewBox={`0 0 ${SIZE} ${SIZE}`}
      className="absolute"
      animate={{ rotate: -360 }}
      transition={{
        duration: 45,
        repeat: Infinity,
        ease: "linear",
      }}
    >
      {nodes.map((node, index) => {
        const rad = (node.angle * Math.PI) / 180;

        const x = CENTER + Math.cos(rad) * node.r;
        const y = CENTER + Math.sin(rad) * node.r;

        return (
          <motion.circle
            key={index}
            cx={x}
            cy={y}
            r={node.size}
            fill="#3DD9FF"
            animate={{
              opacity: [0.4, 1, 0.4],
              scale: [1, 1.35, 1],
            }}
            transition={{
              duration: 2 + index * 0.15,
              repeat: Infinity,
            }}
          />
        );
      })}
    </motion.svg>
  );
}