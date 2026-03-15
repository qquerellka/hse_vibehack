import type { ButtonHTMLAttributes } from 'react'
import { cn } from '../lib/cn'

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'ghost' | 'outline'
}

export function Button({ className, variant = 'primary', ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center rounded-full border px-4 py-2 text-sm transition-transform duration-200 hover:-translate-y-0.5 disabled:cursor-not-allowed disabled:opacity-50',
        variant === 'primary' && 'border-ink bg-ink text-paper',
        variant === 'outline' && 'border-line bg-white/70 text-ink',
        variant === 'ghost' && 'border-transparent bg-transparent text-muted hover:border-line hover:text-ink',
        className,
      )}
      {...props}
    />
  )
}
