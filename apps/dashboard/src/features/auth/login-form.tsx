import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";

const schema = z.object({
  email: z.email(),
  password: z.string().min(8),
});

type FormValues = z.infer<typeof schema>;

export function LoginForm() {
  const form = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const login = useMutation({
    mutationFn: api.login,
  });

  const onSubmit = form.handleSubmit(async (values) => {
    await login.mutateAsync(values);
  });

  return (
    <Card className="w-full max-w-md p-8">
      <div className="mb-8">
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-accent">
          Secure Access
        </p>
        <h1 className="mt-4 text-3xl font-semibold text-primary">
          Client Portal
        </h1>
        <p className="mt-3 text-sm text-slate-600">
          Use your account credentials to access documents and activity.
        </p>
      </div>
      <form className="space-y-4" onSubmit={onSubmit}>
        <div>
          <Input
            type="email"
            placeholder="Email address"
            {...form.register("email")}
          />
          {form.formState.errors.email ? (
            <p className="mt-1 text-sm text-red-600">
              {form.formState.errors.email.message}
            </p>
          ) : null}
        </div>
        <div>
          <Input
            type="password"
            placeholder="Password"
            {...form.register("password")}
          />
          {form.formState.errors.password ? (
            <p className="mt-1 text-sm text-red-600">
              {form.formState.errors.password.message}
            </p>
          ) : null}
        </div>
        <Button
          className="w-full"
          size="lg"
          type="submit"
          disabled={login.isPending}
        >
          {login.isPending ? "Signing in..." : "Sign in"}
        </Button>
        {login.isError ? (
          <p className="text-sm text-red-600">
            Authentication failed. Verify your credentials.
          </p>
        ) : null}
      </form>
    </Card>
  );
}
