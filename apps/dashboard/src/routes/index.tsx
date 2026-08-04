import { createFileRoute } from "@tanstack/react-router";
import { LoginForm } from "@/features/auth/login-form";

export const Route = createFileRoute("/")({
  component: () => (
    <main className="flex min-h-screen items-center justify-center px-6 py-12">
      <LoginForm />
    </main>
  )
});

