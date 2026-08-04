import { motion } from "framer-motion";

const SIZE = 440;
const CENTER = SIZE / 2;
const RADIUS = 195;

export default function RingTicks() {
  const ticks = Array.from({ length: 72 });

  return (
    <motion.svg
      width={SIZE}
      height={SIZE}
      viewBox={`0 0 ${SIZE} ${SIZE}`}
      className="absolute"
      animate={{ rotate: -360 }}
      transition={{
        duration: 120,
        repeat: Infinity,
        ease: "linear",
      }}
    >
      <g transform={`translate(${CENTER}, ${CENTER})`}>
        {ticks.map((_, i) => {
          const angle = (360 / ticks.length) * i;

          return (
            <line
              key={i}
              x1={0}
              y1={-RADIUS}
              x2={0}
              y2={-(RADIUS - (i % 6 === 0 ? 12 : 6))}
              stroke="#4FD8FF"
              strokeWidth={i % 6 === 0 ? 2 : 1}
              opacity={i % 6 === 0 ? 0.9 : 0.35}
              transform={`rotate(${angle})`}
            />
          );
        })}
      </g>
    </motion.svg>
  );
}