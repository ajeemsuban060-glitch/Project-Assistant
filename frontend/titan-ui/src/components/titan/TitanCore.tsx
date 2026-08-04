import TitanLogo from "./TitanLogo";

import GlowLayer from "./effects/GlowLayer";
import PulseRing from "./rings/PulseRing";

import RingOuter from "./rings/OuterRing";
import RingTicks from "./rings/RingTicks";
import HUDRing from "./rings/HUDRing";
import InnerRing from "./rings/InnerRing";
import RingNodes from "./rings/RingNodes";

export default function TitanCore() {
  return (
    <div className="relative flex h-[520px] w-[520px] items-center justify-center">

      {/* Background Glow */}
      <GlowLayer />

      {/* HUD Layers */}
      <RingOuter />

      <RingTicks />

      <HUDRing />

      <RingNodes />

      <PulseRing />

      <InnerRing />

      {/* Center Logo */}
      <TitanLogo />

    </div>
  );
}