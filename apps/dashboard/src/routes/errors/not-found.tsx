import { Link } from "@tanstack/react-router";
import { ArrowLeft } from "lucide-react";

import { Button } from "../../components/ui/button";

export function NotFoundPage() {
  return (
    <main className="grid min-h-screen place-items-center bg-slate-950 px-6 text-white">
      <div className="max-w-lg text-center">
        <p className="text-sm font-semibold uppercase tracking-[0.25em] text-amber-400">
          Error 404
        </p>

        <h1 className="mt-4 text-4xl font-bold tracking-tight">
          Page not found
        </h1>

        <p className="mt-4 text-slate-300">
          The requested dashboard page does not exist or has been moved.
        </p>

        <Button asChild className="mt-8">
          <Link to="/dashboard">
            <ArrowLeft size={16} />
            Return to dashboard
          </Link>
        </Button>
      </div>
    </main>
  );
}
