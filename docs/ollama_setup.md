# Ollama Setup Guide

This guide will help you install and configure Ollama for use with the macOS Tarot App.

## What is Ollama?

Ollama is an open-source tool that simplifies running Large Language Models (LLMs) locally on your Mac. It provides a command-line interface and local API endpoint for interacting with AI models without sending data to external servers.

## Installation

### Method 1: Official Installer (Recommended)

1. **Download Ollama**:
   - Visit [https://ollama.ai](https://ollama.ai)
   - Click "Download for macOS"
   - Run the downloaded installer

2. **Verify Installation**:
   ```bash
   ollama --version
   ```

### Method 2: Homebrew

```bash
brew install ollama
```

### Method 3: Manual Installation

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

## Recommended Models

For the Tarot app, we recommend starting with lightweight models that provide good performance on consumer hardware:

### Primary Recommendation: Llama 3.2 3B

```bash
ollama pull llama3.2:3b
```

**Why this model?**
- Excellent balance of performance and resource usage
- Good at structured output (JSON)
- Fast inference on Apple Silicon
- Sufficient context length for tarot readings

### Alternative Models

**For better performance (if you have more RAM):**
```bash
ollama pull llama3.2:8b
```

**For faster inference (if you have less RAM):**
```bash
ollama pull phi3:3.8b
```

**For specialized tasks:**
```bash
ollama pull mistral:7b
```

## Starting Ollama

### Automatic Start (Recommended)

Ollama should start automatically when you log in. You can verify it's running:

```bash
curl http://localhost:11434/api/tags
```

### Manual Start

If Ollama isn't running automatically:

```bash
ollama serve
```

This will start the Ollama server on `http://localhost:11434`.

## Configuration

### Model Selection in Tarot App

1. Open the Tarot app
2. Go to Settings tab
3. In the "AI Configuration" section:
   - **Model**: Select your preferred model (e.g., `llama3.2:3b`)
   - **Host**: `localhost` (default)
   - **Port**: `11434` (default)

### Performance Tuning

For optimal performance, you can adjust Ollama settings:

```bash
# Set number of threads (adjust based on your CPU)
export OLLAMA_NUM_THREADS=4

# Set GPU layers (if you have a compatible GPU)
export OLLAMA_GPU_LAYERS=20

# Restart Ollama after setting environment variables
ollama serve
```

## Troubleshooting

### Common Issues

**1. "Connection refused" error**
- Ensure Ollama is running: `ollama serve`
- Check if port 11434 is available: `lsof -i :11434`

**2. Model not found**
- Pull the model: `ollama pull llama3.2:3b`
- List available models: `ollama list`

**3. Slow responses**
- Try a smaller model: `ollama pull phi3:3.8b`
- Increase system RAM if possible
- Close other applications to free up resources

**4. Out of memory errors**
- Use a smaller model
- Reduce context length in app settings
- Close other applications

### Checking Ollama Status

```bash
# Check if Ollama is running
ps aux | grep ollama

# Check available models
ollama list

# Test API connectivity
curl http://localhost:11434/api/tags

# Test model generation
ollama run llama3.2:3b "Hello, how are you?"
```

## Privacy and Security

### Local Processing

- All AI processing happens locally on your machine
- No data is sent to external servers
- Your tarot readings remain private

### Network Security

By default, Ollama only accepts connections from localhost. If you need to allow external connections (not recommended for privacy):

```bash
OLLAMA_HOST=0.0.0.0 ollama serve
```

**Warning**: This exposes Ollama to your network. Only do this if you understand the security implications.

## Advanced Configuration

### Custom Model Configuration

You can create custom model configurations:

```bash
# Create a custom model file
cat > Modelfile << EOF
FROM llama3.2:3b
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER max_tokens 2000
EOF

# Create the custom model
ollama create tarot-reader -f Modelfile
```

### Environment Variables

```bash
# Set Ollama data directory
export OLLAMA_MODELS=/path/to/custom/models

# Set Ollama host
export OLLAMA_HOST=localhost:11434

# Set number of threads
export OLLAMA_NUM_THREADS=4
```

## System Requirements

### Minimum Requirements

- **macOS**: 12.0 (Monterey) or later
- **RAM**: 8GB (16GB recommended)
- **Storage**: 4GB free space for models
- **CPU**: Intel or Apple Silicon

### Recommended Requirements

- **macOS**: 13.0 (Ventura) or later
- **RAM**: 16GB or more
- **Storage**: 10GB free space
- **CPU**: Apple Silicon (M1/M2/M3) for best performance

## Getting Help

### Official Resources

- [Ollama Documentation](https://ollama.ai/docs)
- [Ollama GitHub](https://github.com/ollama/ollama)
- [Model Library](https://ollama.ai/library)

### Community Support

- [Ollama Discord](https://discord.gg/ollama)
- [Reddit r/Ollama](https://reddit.com/r/ollama)

### Tarot App Support

If you're having issues specifically with the Tarot app's AI integration:

1. Check the app's Settings tab for error messages
2. Verify Ollama is running and accessible
3. Try a different model
4. Check the app's logs for detailed error information

## Next Steps

Once Ollama is installed and configured:

1. **Test the connection** in the Tarot app Settings tab
2. **Try a reading** to see the AI in action
3. **Experiment with different models** to find your preference
4. **Adjust settings** based on your hardware and preferences

The AI will enhance your tarot readings by providing contextual interpretations, influenced meanings, and thoughtful guidance based on the card interactions in your spreads.