install:
	@echo "🚀 Installing xpander-nemo-agent..."
	pip install build
	pip install -e .
	@echo "🔧 Fixing agno version conflict..."
	pip install --no-deps nvidia-nat-agno
	pip install --force-reinstall "agno>=1.8.2,<2.0"
	@echo "✅ Installation complete! You can now use: nat run --config_file nemo_config.yml --input \"Hello, what can you do?\""
