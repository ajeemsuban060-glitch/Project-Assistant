import { motion } from "framer-motion";
import titanMark from "../../assets/logo/titan-mark.png";

export default function TitanLogo() {
  return (
    <motion.img
      src={titanMark}
      alt="TITAN"
      className="w-72 md:w-80 select-none"
      animate={{ y: [0, -6, 0] }}
      transition={{
        duration: 5,
        repeat: Infinity,
        ease: "easeInOut",
      }}
      draggable={false}
    />
  );
}