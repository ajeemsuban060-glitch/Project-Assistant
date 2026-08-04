import { GlassCard } from "@/components/common";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-[#030712] p-10">
      <GlassCard className="max-w-md p-8">
        <h2 className="text-2xl font-bold text-white">
          TITAN
        </h2>

        <p className="mt-3 text-slate-300">
          Your Right Hand
        </p>
      </GlassCard>
    </div>

    <div className="bg-red-500 text-white p-4">
    Test
</div>
  );
}