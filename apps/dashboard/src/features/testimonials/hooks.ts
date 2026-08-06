import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  deleteTestimonial,
  getTestimonial,
  getTestimonials,
  publishTestimonial,
  scheduleTestimonial,
} from "./api";
import type { TestimonialFilters } from "./types";

export const testimonialsQueryKeys = {
  all: ["testimonials"] as const,
  lists: () => ["testimonials", "list"] as const,
  list: (filters: TestimonialFilters) =>
    [...testimonialsQueryKeys.lists(), filters] as const,
  detail: (testimonialId: string) =>
    ["testimonials", "detail", testimonialId] as const,
};

export function useTestimonials(filters: TestimonialFilters) {
  return useQuery({
    queryKey: testimonialsQueryKeys.list(filters),
    queryFn: () => getTestimonials(filters),
  });
}

export function useTestimonial(testimonialId: string, enabled: boolean) {
  return useQuery({
    queryKey: testimonialsQueryKeys.detail(testimonialId),
    queryFn: () => getTestimonial(testimonialId),
    enabled,
  });
}

function useInvalidateTestimonials() {
  const queryClient = useQueryClient();

  return async () => {
    await queryClient.invalidateQueries({
      queryKey: testimonialsQueryKeys.all,
    });
  };
}

export function usePublishTestimonial() {
  const invalidate = useInvalidateTestimonials();

  return useMutation({
    mutationFn: publishTestimonial,
    onSuccess: invalidate,
  });
}

export function useScheduleTestimonial() {
  const invalidate = useInvalidateTestimonials();

  return useMutation({
    mutationFn: scheduleTestimonial,
    onSuccess: invalidate,
  });
}

export function useDeleteTestimonial() {
  const invalidate = useInvalidateTestimonials();

  return useMutation({
    mutationFn: deleteTestimonial,
    onSuccess: invalidate,
  });
}
