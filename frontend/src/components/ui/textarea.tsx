import * as React from "react"

import { cn } from "@/lib/utils"

function Textarea({ className, ...props }: React.ComponentProps<"textarea">) {
  return (
    <textarea
      data-slot="textarea"
      className={cn(
        "min-h-24 w-full border-[3px] border-foreground bg-input px-4 py-3 text-base placeholder:text-muted-foreground transition-all outline-none resize-none disabled:cursor-not-allowed disabled:opacity-50",
        "focus:shadow-[2px_2px_0_var(--foreground)]",
        className
      )}
      {...props}
    />
  )
}

export { Textarea }
