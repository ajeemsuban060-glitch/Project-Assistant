import AnimatedBackground from "../components/background/AnimatedBackground";
import { TitanCore } from "../components/titan";

export default function HomePage() {
  return (
    <div className="relative min-h-screen overflow-hidden">
      {/* Animated Background */}
      <AnimatedBackground />

      {/* Main Content */}
      <main className="relative z-10 flex min-h-screen flex-col items-center justify-center px-6">

        {/* TITAN Core */}
        <TitanCore />

        {/* Brand Name */}
        <h1 className="mt-8 text-5xl font-extrabold tracking-[0.35em] text-white">
          TITAN
        </h1>

        {/* Tagline */}
        <p className="mt-3 text-sm uppercase tracking-[0.45em] text-cyan-300/80">
          Your Right Hand
        </p>

        {/* Placeholder Panels */}
        <div className="mt-16 grid w-full max-w-6xl gap-8 lg:grid-cols-2">

          {/* Conversation */}
          <div className="rounded-3xl border border-white/10 bg-white/5 p-6 backdrop-blur-xl">
            <h2 className="mb-4 text-xl font-semibold text-white">
              Conversation
            </h2>

            <p className="text-slate-400">
              Hello Boss 👋
            </p>

            <p className="mt-2 text-slate-500">
              Ready whenever you are.
            </p>
          </div>

          {/* Today's Tasks */}
          <div className="rounded-3xl border border-white/10 bg-white/5 p-6 backdrop-blur-xl">
            <h2 className="mb-4 text-xl font-semibold text-white">
              Today's Tasks
            </h2>

            <ul className="space-y-3 text-slate-300">
              <li>✅ Build TITAN Core</li>
              <li>⬜ Connect Backend</li>
              <li>⬜ Voice Assistant</li>
              <li>⬜ Memory Integration</li>
            </ul>
          </div>

        </div>

      </main>
    </div>
  );
}