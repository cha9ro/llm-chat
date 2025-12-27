# CLAUDE.md - Frontend

This file provides guidance to Claude Code when working with the frontend of this repository.

## Technology Stack

- **Framework**: Next.js 15 (App Router)
- **Runtime**: React 18
- **Language**: TypeScript 5.6
- **Package Manager**: pnpm
- **UI Library**: HeroUI v2 (Hero UI component library)
- **Styling**: Tailwind CSS v4 with PostCSS
- **Animations**: Framer Motion
- **Theme**: next-themes (dark mode support)
- **Linting**: ESLint with TypeScript, React, and Prettier plugins

## Development Commands

All commands should be run from the `frontend/` directory:

```bash
# Install dependencies
pnpm install

# Run development server (uses Turbopack)
# Available at: http://localhost:3000
pnpm dev

# Build for production
pnpm build

# Start production server
pnpm start

# Lint and auto-fix
pnpm lint
```

## Project Structure

```
frontend/
├── app/                  # Next.js App Router
│   ├── layout.tsx        # Root layout with providers
│   ├── page.tsx          # Home page
│   ├── error.tsx         # Error boundary
│   └── providers.tsx     # Client-side providers wrapper
├── components/           # Reusable React components
│   ├── navbar.tsx        # Navigation bar component
│   ├── theme-switch.tsx  # Dark/light mode toggle
│   ├── icons.tsx         # Icon components
│   ├── primitives.ts     # Tailwind Variants utilities
│   └── counter.tsx       # Example component
├── config/               # Configuration files
│   ├── site.ts           # Site metadata and navigation
│   └── fonts.ts          # Font configurations
├── styles/               # Global styles
│   └── globals.css       # Global CSS and Tailwind directives
├── types/                # TypeScript type definitions
└── public/               # Static assets
```

## Architecture Patterns

### App Router (Next.js 15)

This project uses Next.js App Router with the `app/` directory structure:

- **Server Components by default**: Components in `app/` are Server Components unless marked with `"use client"`
- **Client Components**: Use `"use client"` directive when:
  - Using React hooks (useState, useEffect, etc.)
  - Using browser APIs
  - Using event handlers
  - Using HeroUI interactive components

Example:
```tsx
"use client";

import { useState } from "react";
import { Button } from "@heroui/button";

export default function Counter() {
  const [count, setCount] = useState(0);
  return <Button onClick={() => setCount(count + 1)}>{count}</Button>;
}
```

### Providers Pattern

The app uses a providers wrapper pattern to initialize client-side libraries:

```tsx
// app/providers.tsx
"use client";

import { HeroUIProvider } from "@heroui/system";
import { ThemeProvider as NextThemesProvider } from "next-themes";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <HeroUIProvider>
      <NextThemesProvider attribute="class" defaultTheme="dark">
        {children}
      </NextThemesProvider>
    </HeroUIProvider>
  );
}
```

This is used in the root layout:
```tsx
// app/layout.tsx
import { Providers } from "./providers";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html suppressHydrationWarning>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

## Styling with Tailwind CSS v4

### Using Tailwind Classes

Apply utility classes directly:

```tsx
<div className="flex items-center gap-4 p-4">
  <h1 className="text-2xl font-bold">Title</h1>
</div>
```

### Using Tailwind Variants

For complex component variants, use `tailwind-variants`:

```tsx
// components/primitives.ts
import { tv } from "tailwind-variants";

export const buttonVariants = tv({
  base: "inline-flex items-center justify-center rounded-md",
  variants: {
    color: {
      primary: "bg-blue-500 text-white",
      secondary: "bg-gray-500 text-white",
    },
    size: {
      sm: "px-3 py-1 text-sm",
      md: "px-4 py-2 text-base",
    },
  },
  defaultVariants: {
    color: "primary",
    size: "md",
  },
});
```

### Global Styles

Global styles are defined in `styles/globals.css`:
- Tailwind directives (`@import`, `@layer`)
- CSS custom properties for theming
- Global resets

## HeroUI Components

HeroUI is the primary component library. Import components individually:

```tsx
import { Button } from "@heroui/button";
import { Card, CardBody, CardHeader } from "@heroui/card";
import { Input } from "@heroui/input";
import { Modal, ModalContent, ModalHeader, ModalBody } from "@heroui/modal";
```

**Note**: HeroUI components are client-side components and require `"use client"` directive.

Common components:
- **Layout**: Card, Divider, Spacer, Drawer
- **Forms**: Input, Select, Autocomplete, Switch, Radio
- **Buttons**: Button, Link, Kbd
- **Display**: Avatar, Badge, Chip, Image, Skeleton, Spinner
- **Overlays**: Modal, Popover, Tooltip, Dropdown
- **Navigation**: Navbar, Tabs, Pagination
- **Data**: Table, Listbox, Accordion

## Theme and Dark Mode

### Theme Configuration

The app uses `next-themes` for theme management:

```tsx
import { useTheme } from "next-themes";

export function ThemeSwitch() {
  const { theme, setTheme } = useTheme();

  return (
    <button onClick={() => setTheme(theme === "dark" ? "light" : "dark")}>
      Toggle theme
    </button>
  );
}
```

### Theme Persistence

- Theme is persisted in localStorage
- `suppressHydrationWarning` on `<html>` prevents hydration mismatch
- `attribute="class"` applies theme via CSS class on html element

## TypeScript Conventions

### Type Definitions

Place shared types in the `types/` directory:

```tsx
// types/chat.ts
export interface Chat {
  id: string;
  userId: string;
  title: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface Message {
  id: string;
  chatId: string;
  role: "user" | "assistant" | "system";
  content: string;
  createdAt: string;
}
```

### Component Props

Define props interfaces inline or separately:

```tsx
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: "primary" | "secondary";
}

export function CustomButton({ label, onClick, variant = "primary" }: ButtonProps) {
  return <button onClick={onClick}>{label}</button>;
}
```

## API Integration

### Fetching from Backend

Use Next.js patterns for data fetching:

**Server Component (recommended for initial data):**
```tsx
// app/chats/page.tsx
async function getChats(userId: string) {
  const res = await fetch(`http://localhost:8000/chats?user_id=${userId}`, {
    cache: 'no-store' // or 'force-cache' for static data
  });
  return res.json();
}

export default async function ChatsPage() {
  const chats = await getChats("user123");
  return <div>{/* render chats */}</div>;
}
```

**Client Component (for dynamic interactions):**
```tsx
"use client";

import { useEffect, useState } from "react";

export function ChatList() {
  const [chats, setChats] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/chats?user_id=user123")
      .then(res => res.json())
      .then(setChats);
  }, []);

  return <div>{/* render chats */}</div>;
}
```

### Environment Variables

For API URLs, use environment variables:

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Access in code:
```tsx
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
```

**Note**: Only `NEXT_PUBLIC_*` variables are exposed to the browser.

## Development Guidelines

### Component Organization

- **Pages**: Place in `app/` directory using Next.js routing conventions
- **Reusable components**: Place in `components/` directory
- **Layout components**: Use `layout.tsx` files in `app/` subdirectories
- **Loading states**: Use `loading.tsx` files in `app/` subdirectories
- **Error boundaries**: Use `error.tsx` files in `app/` subdirectories

### File Naming

- Use `.tsx` for components with JSX
- Use `.ts` for utilities and types without JSX
- Use kebab-case for file names: `chat-list.tsx`, `theme-switch.tsx`
- Use PascalCase for component names: `ChatList`, `ThemeSwitch`

### Import Order

Follow this import order (enforced by ESLint):
1. React imports
2. Third-party libraries
3. HeroUI components
4. Local components
5. Utilities and types
6. Styles

### Accessibility

HeroUI components include built-in accessibility features. Ensure:
- Proper semantic HTML
- ARIA labels where needed
- Keyboard navigation support
- Focus management in modals/drawers

## Linting and Formatting

### ESLint Configuration

Configured via `eslint.config.mjs` with:
- TypeScript support
- React and React Hooks rules
- Next.js specific rules
- Import order enforcement
- Unused imports detection
- Prettier integration

### Prettier Configuration

Configured via `.prettierrc`:
- Automatic code formatting
- Tailwind CSS class sorting (via `prettier-plugin-tailwindcss`)

Run linting:
```bash
pnpm lint       # Check and auto-fix
```

## pnpm Configuration

The `.npmrc` file contains important pnpm configuration:

```
public-hoist-pattern[]=*@heroui/*
```

This ensures HeroUI packages are properly hoisted for peer dependency resolution.

**Important**: After modifying `.npmrc`, run `pnpm install` again.
