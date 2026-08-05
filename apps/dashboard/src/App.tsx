import { Button } from "./components/ui/button";

function App() {
  return (
    <main className="min-h-screen bg-slate-950 px-6 py-20 text-white">
      <div className="mx-auto max-w-4xl">
        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-amber-400">
          LKProfessionals Dashboard
        </p>

        <h1 className="mt-4 text-4xl font-bold tracking-tight">
          Dashboard foundation is working.
        </h1>

        <p className="mt-4 max-w-2xl text-slate-300">
          React, TypeScript, Tailwind, Radix UI, and reusable component utilities
          are now connected.
        </p>

        <div className="mt-8 flex flex-wrap gap-4">
          <Button>Primary action</Button>
          <Button variant="secondary">Secondary</Button>
          <Button variant="outline">Outline</Button>
          <Button variant="destructive">Delete</Button>
        </div>
      </div>
    </main>
  );
}

export default App;
