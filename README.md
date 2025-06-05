# Direct Text-to-Website Generator

A Python-based tool that generates complete Next.js websites directly from text descriptions using OpenAI's GPT-4, without relying on `create-next-app`.

## 🚀 Features

- **Direct Generation**: Creates Next.js projects without using `create-next-app`
- **AI-Powered**: Uses GPT-4 Turbo for intelligent code generation
- **Modern Stack**: Next.js 15+ with App Router, TypeScript, and Tailwind CSS
- **Production Ready**: Generates clean, responsive, and accessible websites
- **Complete Setup**: Includes all configuration files and dependencies

## 📋 Prerequisites

- Python 3.7+
- OpenAI API key
- Node.js 18+ (for running the generated website)
- npm or yarn (for dependency management)

## 🛠️ Installation

1. **Clone or download the script**
   ```bash
   # Save the script as text_to_website.py
   ```

2. **Install Python dependencies**
   ```bash
   pip install openai pathlib dataclasses argparse
   ```

3. **Set up OpenAI API key**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   # or pass it as a command line argument
   ```

## 📖 Usage

### Basic Usage

```bash
python text_to_website.py -i "Create a modern landing page for a tech startup"
```

### Advanced Usage

```bash
python text_to_website.py \
  --input "Build a portfolio website with hero section, projects gallery, and contact form" \
  --project-name "my-portfolio" \
  --output-dir "./projects" \
  --api-key "your-api-key"
```

### Using a Text File as Input

```bash
python text_to_website.py -i "./website_description.txt" -p "my-website"
```

## 🎯 Command Line Arguments

| Argument | Short | Required | Description | Default |
|----------|-------|----------|-------------|---------|
| `--input` | `-i` | ✅ | Input text description or file path | - |
| `--project-name` | `-p` | ❌ | Name of the generated project | `generated-website` |
| `--output-dir` | `-o` | ❌ | Directory to create the project in | `./output` |
| `--api-key` | `-k` | ❌ | OpenAI API key (can use env var) | `OPENAI_API_KEY` |

## 📁 Generated Project Structure

```
generated-website/
├── src/
│   ├── app/
│   │   ├── globals.css          # Global styles with CSS variables
│   │   ├── layout.tsx           # Root layout with metadata
│   │   └── page.tsx             # Main page component (AI-generated)
│   └── components/              # Directory for additional components
├── public/                      # Static assets directory
├── package.json                 # Dependencies and scripts
├── next.config.js              # Next.js configuration
├── tailwind.config.js          # Tailwind CSS configuration
├── postcss.config.js           # PostCSS configuration
├── tsconfig.json               # TypeScript configuration
├── .eslintrc.json              # ESLint configuration
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
```

## 🔧 Generated Project Dependencies

### Core Dependencies
- **Next.js 15.0.3**: React framework with App Router
- **React 18.3.1**: UI library
- **TypeScript 5.6.0**: Type-safe JavaScript
- **Tailwind CSS 3.4.14**: Utility-first CSS framework

### Development Dependencies
- **ESLint**: Code linting and formatting
- **PostCSS & Autoprefixer**: CSS processing
- **Inter Font**: Modern typography

## 🚀 Running the Generated Website

After generation, navigate to your project and run:

```bash
cd output/generated-website
npm install
npm run dev
```

Your website will be available at `http://localhost:3000`

## 🎨 Features of Generated Websites

### Modern Design System
- **CSS Variables**: Custom properties for theming
- **Glassmorphism**: Modern UI effects with backdrop-blur
- **Responsive Design**: Mobile-first approach
- **Smooth Animations**: Fade-in, slide-up, and bounce effects
- **Custom Components**: Pre-styled buttons, cards, and layouts

### Technical Features
- **TypeScript**: Full type safety
- **App Router**: Latest Next.js routing system
- **Server Components**: Optimized performance by default
- **Client Components**: Interactive features when needed
- **SEO Ready**: Proper metadata and semantic HTML
- **Accessibility**: WCAG compliant markup

## 🔍 Code Generation Intelligence

The AI system is optimized to:

- **Detect Client-Side Features**: Automatically adds `'use client'` directive when needed
- **Follow Next.js 15 Conventions**: Uses App Router patterns and best practices
- **Generate Clean TypeScript**: Proper interfaces and type annotations
- **Create Responsive Layouts**: Mobile-first Tailwind classes
- **Include Modern UI Patterns**: Gradients, animations, and interactive elements

## 📝 Example Input Prompts

### Simple Website
```
"Create a personal blog homepage with a header, hero section, and recent posts"
```

### Business Website
```
"Build a SaaS landing page with pricing tiers, feature comparison, and testimonials"
```

### Portfolio Website
```
"Design a creative portfolio with image gallery, about section, and contact form"
```

### E-commerce
```
"Create a product showcase page with grid layout, filters, and shopping cart"
```

## 🐛 Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   ```bash
   # Set environment variable
   export OPENAI_API_KEY="your-key-here"
   ```

2. **Permission Errors**
   ```bash
   # Check directory permissions
   chmod 755 ./output
   ```

3. **Node.js Version Issues**
   ```bash
   # Use Node.js 18+
   node --version
   ```

4. **Dependency Installation Fails**
   ```bash
   # Clear npm cache
   npm cache clean --force
   rm -rf node_modules
   npm install
   ```

## 🔒 Security Considerations

- **API Key Protection**: Never commit API keys to version control
- **Input Validation**: The script validates and sanitizes input
- **Safe File Operations**: Uses Path objects for secure file handling
- **Error Handling**: Comprehensive error catching and logging

## 🤝 Contributing

To improve the generator:

1. **Model Updates**: Modify the system prompt for better output
2. **Configuration**: Add new Next.js or Tailwind features
3. **Templates**: Extend the base template system
4. **Error Handling**: Improve robustness and user experience

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues and questions:

1. Check the troubleshooting section
2. Review generated project logs
3. Verify OpenAI API quota and permissions
4. Ensure all prerequisites are installed

## 🔮 Future Enhancements

- **Multiple Pages**: Generate multi-page websites
- **Component Library**: Custom component generation
- **Database Integration**: Add backend functionality
- **Deployment**: Automatic Vercel/Netlify deployment
- **Theme System**: Multiple design system support
