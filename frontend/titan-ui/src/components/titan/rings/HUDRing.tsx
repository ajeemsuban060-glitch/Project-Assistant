import { motion } from "framer-motion";

const SIZE = 420;
const C = SIZE / 2;

export default function HUDRing() {
  return (
    <svg
      width={SIZE}
      height={SIZE}
      viewBox={`0 0 ${SIZE} ${SIZE}`}
      className="absolute overflow-visible"
    >
      <defs>
        <filter id="cyanGlow">
          <feGaussianBlur stdDeviation="3" result="blur" />
          <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      {/* Layer 1 */}
      <motion.g
        style={{ originX: "50%", originY: "50%" }}
        animate={{ rotate: 360 }}
        transition={{
          duration: 90,
          repeat: Infinity,
          ease: "linear",
        }}
      >
        <circle
          cx={C}
          cy={C}
          r="188"
          fill="none"
          stroke="#36D7FF"
          strokeWidth="2"
          opacity="0.15"
        />

        <circle
          cx={C}
          cy={C}
          r="178"
          fill="none"
          stroke="#36D7FF"
          strokeWidth="5"
          strokeDasharray="48 16"
          strokeLinecap="round"
          filter="url(#cyanGlow)"
        />
      </motion.g>

      {/* Layer 2 */}
      <motion.g
        style={{ originX: "50%", originY: "50%" }}
        animate={{ rotate: -360 }}
        transition={{
          duration: 55,
          repeat: Infinity,
          ease: "linear",
        }}
      >
        <circle
          cx={C}
          cy={C}
          r="160"
          fill="none"
          stroke="#7B61FF"
          strokeWidth="3"
          strokeDasharray="18 12"
          strokeLinecap="round"
          opacity="0.8"
        />

        <circle
          cx={C}
          cy={C}
          r="148"
          fill="none"
          stroke="#36D7FF"
          strokeWidth="2"
          strokeDasharray="4 8"
          opacity="0.45"
        />
      </motion.g>

      {/* Layer 3 */}
      <motion.g
        style={{ originX: "50%", originY: "50%" }}
        animate={{ rotate: 360 }}
        transition={{
          duration: 28,
          repeat: Infinity,
          ease: "linear",
        }}
      >
        <circle
          cx={C}
          cy={C}
          r="128"
          fill="none"
          stroke="#36D7FF"
          strokeWidth="2"
          strokeDasharray="2 10"
          opacity="0.7"
        />
      </motion.g>

      {/* Four glowing nodes */}
      <motion.g
        style={{ originX: "50%", originY: "50%" }}
        animate={{ rotate: -360 }}
        transition={{
          duration: 18,
          repeat: Infinity,
          ease: "linear",
        }}
      >
        <circle cx={C} cy="50" r="4" fill="#36D7FF" />
        <circle cx="50" cy={C} r="4" fill="#36D7FF" />
        <circle cx={C} cy="370" r="4" fill="#36D7FF" />
        <circle cx="370" cy={C} r="4" fill="#36D7FF" />
      </motion.g>
    </svg>
  );
}