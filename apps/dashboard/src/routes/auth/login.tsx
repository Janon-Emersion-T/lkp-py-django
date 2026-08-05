import { Navigate } from "@tanstack/react-router";

import { LoginForm } from "../../features/auth/login-form";
import { useAuth } from "../../features/auth/auth-context";

export function LoginPage() {
  const {
    isAuthenticated,
    isLoading,
  } = useAuth();

  if (isLoading) {
    return (
      <main className="grid min-h-screen place-items-center bg-slate-950 text-white">
        <p>Checking session...</p>
      </main>
    );
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" />;
  }

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-20 text-white">
      <div className="mx-auto max-w-md">
        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-amber-400">
          LKProfessionals
        </p>

        <h1 className="mt-4 text-4xl font-bold tracking-tight">
          Sign in
        </h1>

        <p className="mt-3 text-slate-300">
          Access the LKProfessionals dashboard.
        </p>

        <LoginForm />
      </div>
    </main>
  );
}
