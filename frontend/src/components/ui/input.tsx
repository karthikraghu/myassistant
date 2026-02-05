import * as React from "react"

import { cn } from "@/lib/utils"

function Input({ className, type, ...props }: React.ComponentProps<"input">) {
  return (
    <input
      type={type}
      data-slot="input"
      className={cn(
        "h-10 w-full min-w-0 border-[3px] border-foreground bg-input px-4 py-2 text-base placeholder:text-muted-foreground transition-all outline-none disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50",
        "focus:shadow-[2px_2px_0_var(--foreground)]",
        className
      )}
      {...props}
    />
  )
}

export { Input }
