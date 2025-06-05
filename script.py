#!/usr/bin/env python3
"""
Direct Text-to-Website Generator
Creates Next.js files directly without using create-next-app
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import openai
from openai import OpenAI
import argparse
import logging
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ProjectConfig:
    """Configuration for the website project"""
    project_name: str
    output_dir: str
    openai_api_key: str

class DirectWebsiteGenerator:
    """Generate Next.js website files directly"""
    
    def __init__(self, config: ProjectConfig):
        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key)
        self.project_path = Path(config.output_dir) / config.project_name
        
    def create_system_prompt(self) -> str:
        """Create system prompt for website generation"""
        return """You are an expert Next.js 14+ developer specializing in creating modern, responsive websites using the App Router.

CRITICAL REQUIREMENTS:
1. Generate clean, production-ready Next.js/React code for Next.js 14+ App Router
2. Use TypeScript and Tailwind CSS
3. Output ONLY the code - NO explanations, NO markdown formatting
4. Always add 'use client'; directive at the top if using ANY client-side features (useState, useEffect, event handlers, etc.)
5. Never use next/head in App Router - metadata should be handled in layout.tsx
6. Create beautiful, modern UI with proper styling
7. Ensure responsive design (mobile-first)
8. Use React hooks and best practices
9. Include proper imports and exports

NEXT.JS APP ROUTER RULES:
- Components are Server Components by default
- Add 'use client'; at the very top if using: useState, useEffect, onClick, onChange, onSubmit, etc.
- Don't use next/head - use metadata export in layout files instead
- Use proper TypeScript interfaces
- Follow App Router conventions

STYLING GUIDELINES:
- Use Tailwind CSS for all styling
- Create beautiful gradients and modern colors
- Include hover effects and transitions
- Use proper spacing and typography
- Make it visually appealing and professional
- Use modern design patterns (glassmorphism, subtle animations)

OUTPUT FORMAT:
Generate a complete Next.js page component with:
1. 'use client'; directive if needed (VERY IMPORTANT)
2. All necessary imports
3. TypeScript interfaces if needed
4. Functional component with hooks (if client-side)
5. Beautiful JSX with Tailwind classes
6. Responsive design
7. Modern UI elements
8. Proper error handling for forms

EXAMPLE STRUCTURE:
```typescript
'use client'; // Only if using client-side features

import { useState } from 'react';

export default function HomePage() {
  // Component logic here
  return (
    <div>
      {/* JSX here */}
    </div>
  );
}
```

Remember: Output ONLY the React component code, no explanations, no markdown formatting."""

    def generate_website_code(self, text_input: str) -> str:
        """Generate website code using GPT-4"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-2024-04-09",  # Updated to latest model
                messages=[
                    {"role": "system", "content": self.create_system_prompt()},
                    {"role": "user", "content": f"Create a Next.js App Router page component for: {text_input}. Make it modern, beautiful, and fully functional. Include proper client-side interactivity if needed."}
                ],
                temperature=0.1,
                max_tokens=4000,  # Increased for more complex components
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            generated_code = response.choices[0].message.content.strip()
            
            # Clean up markdown formatting if present
            if generated_code.startswith('```'):
                lines = generated_code.split('\n')
                if lines[0].startswith('```'):
                    lines = lines[1:]
                if lines and lines[-1].startswith('```'):
                    lines = lines[:-1]
                generated_code = '\n'.join(lines)
            
            # Ensure 'use client' is added if client-side features are detected
            client_features = ['useState', 'useEffect', 'onClick', 'onChange', 'onSubmit', 'onFocus', 'onBlur']
            if any(feature in generated_code for feature in client_features) and not generated_code.startswith("'use client'"):
                generated_code = "'use client';\n\n" + generated_code
            
            return generated_code
            
        except Exception as e:
            logger.error(f"Error generating code: {e}")
            raise

    def create_project_structure(self) -> bool:
        """Create the Next.js project structure"""
        try:
            logger.info("Creating project structure...")
            
            # Remove existing directory if it exists
            if self.project_path.exists():
                import shutil
                shutil.rmtree(self.project_path)
            
            # Create directory structure
            directories = [
                self.project_path,
                self.project_path / "src",
                self.project_path / "src" / "app",
                self.project_path / "src" / "components",
                self.project_path / "public"
            ]
            
            for directory in directories:
                directory.mkdir(parents=True, exist_ok=True)
            
            logger.info("Project structure created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error creating project structure: {e}")
            return False

    def create_package_json(self) -> bool:
        """Create package.json file with updated dependencies"""
        try:
            package_json = {
                "name": self.config.project_name,
                "version": "0.1.0",
                "private": True,
                "scripts": {
                    "dev": "next dev",
                    "build": "next build",
                    "start": "next start",
                    "lint": "next lint"
                },
                "dependencies": {
                    "react": "^18.3.1",
                    "react-dom": "^18.3.1",
                    "next": "^15.0.3",
                    "@types/node": "^22.0.0",
                    "@types/react": "^18.3.12",
                    "@types/react-dom": "^18.3.1",
                    "typescript": "^5.6.0",
                    "tailwindcss": "^3.4.14",
                    "autoprefixer": "^10.4.20",
                    "postcss": "^8.4.47",
                    "eslint": "^9.0.0",
                    "eslint-config-next": "^15.0.3",
                    "@eslint/config-array": "^0.18.0",
                    "@eslint/object-schema": "^2.1.4"
                },
                "devDependencies": {
                    "@eslint/js": "^9.0.0",
                    "globals": "^15.0.0"
                }
            }
            
            with open(self.project_path / "package.json", 'w') as f:
                json.dump(package_json, f, indent=2)
            
            logger.info("package.json created with updated dependencies")
            return True
            
        except Exception as e:
            logger.error(f"Error creating package.json: {e}")
            return False

    def create_next_config(self) -> bool:
        """Create next.config.js for Next.js 15"""
        try:
            next_config = """/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: false,
  },
}

module.exports = nextConfig
"""
            
            with open(self.project_path / "next.config.js", 'w') as f:
                f.write(next_config)
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating next.config.js: {e}")
            return False

    def create_tailwind_config(self) -> bool:
        """Create Tailwind CSS configuration"""
        try:
            tailwind_config = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.5s ease-out',
        'bounce-slow': 'bounce 2s infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
"""
            
            with open(self.project_path / "tailwind.config.js", 'w') as f:
                f.write(tailwind_config)
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating tailwind.config.js: {e}")
            return False

    def create_postcss_config(self) -> bool:
        """Create PostCSS configuration"""
        try:
            postcss_config = """module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""
            
            with open(self.project_path / "postcss.config.js", 'w') as f:
                f.write(postcss_config)
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating postcss.config.js: {e}")
            return False

    def create_typescript_config(self) -> bool:
        """Create TypeScript configuration for Next.js 15"""
        try:
            ts_config = {
                "compilerOptions": {
                    "target": "ES2017",
                    "lib": ["dom", "dom.iterable", "ES6"],
                    "allowJs": True,
                    "skipLibCheck": True,
                    "strict": True,
                    "noEmit": True,
                    "esModuleInterop": True,
                    "module": "esnext",
                    "moduleResolution": "bundler",
                    "resolveJsonModule": True,
                    "isolatedModules": True,
                    "jsx": "preserve",
                    "incremental": True,
                    "plugins": [
                        {
                            "name": "next"
                        }
                    ],
                    "baseUrl": ".",
                    "paths": {
                        "@/*": ["./src/*"]
                    }
                },
                "include": [
                    "next-env.d.ts",
                    "**/*.ts",
                    "**/*.tsx",
                    ".next/types/**/*.ts"
                ],
                "exclude": ["node_modules"]
            }
            
            with open(self.project_path / "tsconfig.json", 'w') as f:
                json.dump(ts_config, f, indent=2)
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating tsconfig.json: {e}")
            return False

    def create_globals_css(self) -> bool:
        """Create global CSS file"""
        try:
            globals_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 221.2 83.2% 53.3%;
    --radius: 0.75rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 224.3 76.3% 94.0%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
    font-feature-settings: "rlig" 1, "calt" 1;
  }
}

@layer components {
  .btn {
    @apply inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50;
    @apply h-10 px-4 py-2;
  }
  
  .btn-primary {
    @apply bg-primary text-primary-foreground hover:bg-primary/90;
  }
  
  .btn-secondary {
    @apply bg-secondary text-secondary-foreground hover:bg-secondary/80;
  }
  
  .card {
    @apply rounded-lg border bg-card text-card-foreground shadow-sm;
  }

  .glass {
    @apply backdrop-blur-md bg-white/10 border border-white/20;
  }

  .gradient-text {
    @apply bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent;
  }
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: hsl(var(--muted));
}

::-webkit-scrollbar-thumb {
  background: hsl(var(--primary));
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: hsl(var(--primary) / 0.8);
}
"""
            
            with open(self.project_path / "src" / "app" / "globals.css", 'w') as f:
                f.write(globals_css)
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating globals.css: {e}")
            return False

    def create_layout_file(self) -> bool:
        """Create the root layout file"""
        try:
            layout_content = """import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Generated Website',
  description: 'AI-generated website using Next.js and Tailwind CSS',
  viewport: 'width=device-width, initial-scale=1',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
"""
            
            with open(self.project_path / "src" / "app" / "layout.tsx", 'w') as f:
                f.write(layout_content)
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating layout.tsx: {e}")
            return False

    def create_page_file(self, generated_code: str) -> bool:
        """Create the main page file with generated code"""
        try:
            with open(self.project_path / "src" / "app" / "page.tsx", 'w') as f:
                f.write(generated_code)
            
            logger.info("Main page created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error creating page.tsx: {e}")
            return False

    def create_eslint_config(self) -> bool:
        """Create modern ESLint configuration"""
        try:
            eslint_config = {
                "extends": [
                    "next/core-web-vitals",
                    "next/typescript"
                ],
                "rules": {
                    "@typescript-eslint/no-unused-vars": "warn",
                    "react-hooks/exhaustive-deps": "warn"
                }
            }
            
            with open(self.project_path / ".eslintrc.json", 'w') as f:
                json.dump(eslint_config, f, indent=2)
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating .eslintrc.json: {e}")
            return False

    def create_gitignore(self) -> bool:
        """Create .gitignore file"""
        try:
            gitignore_content = """# Dependencies
/node_modules
/.pnp
.pnp.js
.yarn/install-state.gz

# Testing
/coverage

# Next.js
/.next/
/out/

# Production
/build

# Misc
.DS_Store
*.pem

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Local env files
.env*.local
.env

# Vercel
.vercel

# TypeScript
*.tsbuildinfo
next-env.d.ts

# IDE
.vscode/
.idea/
*.swp
*.swo
"""
            
            with open(self.project_path / ".gitignore", 'w') as f:
                f.write(gitignore_content)
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating .gitignore: {e}")
            return False

    def create_readme(self) -> bool:
        """Create README.md file"""
        try:
            readme_content = f"""# {self.config.project_name}

This is a Next.js project generated by the AI Text-to-Website Generator.

## Getting Started

First, install dependencies:

```bash
npm install
# or
yarn install
# or
pnpm install
```

Then, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Technologies Used

- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **ESLint** - Code linting

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/deployment) for more details.
"""
            
            with open(self.project_path / "README.md", 'w') as f:
                f.write(readme_content)
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating README.md: {e}")
            return False

    def generate_website(self, text_input: str) -> bool:
        """Generate complete website from text input"""
        try:
            logger.info("Starting direct website generation...")
            
            # Step 1: Generate code using GPT-4
            logger.info("Generating code with GPT-4...")
            generated_code = self.generate_website_code(text_input)
            
            # Step 2: Create project structure
            if not self.create_project_structure():
                return False
            
            # Step 3: Create configuration files
            logger.info("Creating configuration files...")
            if not self.create_package_json():
                return False
            if not self.create_next_config():
                return False
            if not self.create_tailwind_config():
                return False
            if not self.create_postcss_config():
                return False
            if not self.create_typescript_config():
                return False
            if not self.create_eslint_config():
                return False
            if not self.create_gitignore():
                return False
            if not self.create_readme():
                return False
            
            # Step 4: Create app files
            logger.info("Creating app files...")
            if not self.create_globals_css():
                return False
            if not self.create_layout_file():
                return False
            if not self.create_page_file(generated_code):
                return False
            
            logger.info(f"Website generation completed successfully!")
            logger.info(f"Project location: {self.project_path}")
            logger.info("To run the project:")
            logger.info(f"  cd {self.project_path}")
            logger.info("  npm install")
            logger.info("  npm run dev")
            
            return True
            
        except Exception as e:
            logger.error(f"Error in website generation: {e}")
            return False

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Direct Text-to-Website Generator")
    parser.add_argument("--input", "-i", required=True, help="Input text description")
    parser.add_argument("--output-dir", "-o", default="./output", help="Output directory")
    parser.add_argument("--project-name", "-p", default="generated-website", help="Project name")
    parser.add_argument("--api-key", "-k", help="OpenAI API key (or set OPENAI_API_KEY env var)")
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OpenAI API key is required. Use --api-key or set OPENAI_API_KEY environment variable.")
        return
    
    # Read input text
    if os.path.isfile(args.input):
        with open(args.input, 'r', encoding='utf-8') as f:
            text_input = f.read()
    else:
        text_input = args.input
    
    # Clean project name
    project_name = args.project_name.lower().replace(' ', '-').replace('_', '-')
    
    # Create configuration
    config = ProjectConfig(
        project_name=project_name,
        output_dir=args.output_dir,
        openai_api_key=api_key
    )
    
    # Generate website
    generator = DirectWebsiteGenerator(config)
    success = generator.generate_website(text_input)
    
    if success:
        print(f"\n✅ Website generated successfully!")
        print(f"📁 Project location: {Path(args.output_dir) / project_name}")
        print(f"\n🚀 To run your website:")
        print(f"   cd {Path(args.output_dir) / project_name}")
        print(f"   npm install")
        print(f"   npm run dev")
        print(f"\n🌐 Your website will be available at: http://localhost:3000")
    else:
        print(f"\n❌ Website generation failed. Check logs for details.")

if __name__ == "__main__":
    main()