export const Schema = z.object({
  phase: z.enum(["select_character", "select_scenario", "playing"]),
  selected_character: z.enum(["", "airine", "bathsheba", "lena", "meme", "belzeebul"]),
  selected_scenario: z.coerce.number().min(0).max(5),
});

export type Schema = z.output<typeof Schema>;
