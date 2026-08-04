import { motion } from "framer-motion";
import { ReactNode } from "react";
import clsx from "clsx";

interface GlassCardProps {
  children: ReactNode;
  className?: string;
}

export default function GlassCard({
  children,
  className,
}: GlassCardProps) {
  return (
    <motion.div
      whileHover={{
        y: -4,
        scale: 1.01,
      }}
      transition={{
        duration: 0.25,
        ease: "easeOut",
      }}
      className={clsx(
        `
        relative
        overflow-hidden
        rounded-3xl

        border
        border-white/10

        bg-white/[0.05]
        backdrop-blur-2xl

        shadow-[0_0_40px_rgba(54,215,255,0.08)]

        before:absolute
        before:inset-0
        before:bg-gradient-to-br
        before:from-white/10
        before:via-transparent
        before:to-transparent
        before:pointer-events-none

        after:absolute
        after:inset-0
        after:rounded-3xl
        after:border
        after:border-cyan-400/5

        transition-all
        duration-300
        `,
        className
      )}
    >
      <div className="relative z-10">
        {children}
      </div>
    </motion.div>
  );
}