import {
  BriefcaseBusiness,
  FolderKanban,
  TrendingUp,
  Users,
} from "lucide-react";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "../../components/ui/card";
import { useAuth } from "../../features/auth/auth-context";

const statistics = [
  {
    label: "Active leads",
    value: "0",
    description: "No leads recorded yet",
    icon: TrendingUp,
  },
  {
    label: "Active projects",
    value: "0",
    description: "No active projects yet",
    icon: FolderKanban,
  },
  {
    label: "Clients",
    value: "0",
    description: "No clients recorded yet",
    icon: BriefcaseBusiness,
  },
  {
    label: "System users",
    value: "1",
    description: "One administrator",
    icon: Users,
  },
] as const;

export function DashboardPage() {
  const { user } = useAuth();

  const displayName =
    [user?.first_name, user?.last_name]
      .filter(Boolean)
      .join(" ") || user?.email;

  return (
    <section>
      <p className="text-sm font-semibold uppercase tracking-[0.2em] text-amber-600">
        Overview
      </p>

      <h1 className="mt-3 text-3xl font-bold tracking-tight text-slate-950">
        Welcome, {displayName}.
      </h1>

      <p className="mt-3 text-slate-600">
        Monitor LKProfessionals operations, leads, clients, and projects.
      </p>

      <div className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {statistics.map((statistic) => {
          const Icon = statistic.icon;

          return (
            <Card key={statistic.label}>
              <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle>{statistic.label}</CardTitle>

                <div className="rounded-lg bg-blue-50 p-2 text-blue-700">
                  <Icon size={18} />
                </div>
              </CardHeader>

              <CardContent>
                <p className="text-3xl font-bold text-slate-950">
                  {statistic.value}
                </p>

                <p className="mt-2 text-sm text-slate-500">
                  {statistic.description}
                </p>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </section>
  );
}
