#!/usr/bin/env python3
"""
iOS Self-Installer Web Server
Serves the IPA file and beautiful installation interface for iPad
"""

import os
import json
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
from pathlib import Path

class IPAServerHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler for serving IPA files and web interface"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '':
            self.serve_index()
        elif self.path == '/manifest.plist':
            self.serve_manifest()
        elif self.path.endswith('.ipa'):
            self.serve_ipa()
        elif self.path == '/api/status':
            self.serve_status()
        elif self.path == '/api/files':
            self.serve_files_list()
        else:
            super().do_GET()
    
    def serve_index(self):
        """Serve the HTML installation page"""
        html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>iOS Self-Installer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 500px;
            width: 100%;
            padding: 40px;
            text-align: center;
        }
        
        .header {
            margin-bottom: 30px;
        }
        
        .icon {
            width: 80px;
            height: 80px;
            margin: 0 auto 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
        }
        
        .subtitle {
            color: #666;
            font-size: 14px;
        }
        
        .info-box {
            background: #f5f5f5;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin: 20px 0;
            border-radius: 8px;
            text-align: left;
        }
        
        .info-box p {
            color: #333;
            font-size: 13px;
            line-height: 1.6;
        }
        
        .button-group {
            display: flex;
            gap: 10px;
            margin-top: 30px;
            flex-direction: column;
        }
        
        .btn {
            padding: 14px 28px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            min-height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }
        
        .btn-primary:active {
            transform: translateY(0);
        }
        
        .btn-primary:disabled {
            opacity: 0.7;
            cursor: not-allowed;
        }
        
        .btn-secondary {
            background: #e0e0e0;
            color: #333;
        }
        
        .btn-secondary:hover {
            background: #d0d0d0;
        }
        
        .status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 10px;
            display: none;
        }
        
        .status.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
            display: block;
        }
        
        .status.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
            display: block;
        }
        
        .status.info {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
            display: block;
        }
        
        .status.warning {
            background: #fff3cd;
            color: #856404;
            border: 1px solid #ffeeba;
            display: block;
        }
        
        .steps {
            text-align: left;
            margin: 25px 0;
        }
        
        .steps h3 {
            color: #333;
            margin-bottom: 15px;
            font-size: 16px;
        }
        
        .step {
            display: flex;
            margin-bottom: 12px;
            align-items: flex-start;
        }
        
        .step-number {
            background: #667eea;
            color: white;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 12px;
            flex-shrink: 0;
            font-size: 12px;
            font-weight: bold;
        }
        
        .step-text {
            color: #333;
            font-size: 13px;
            line-height: 1.5;
        }
        
        .progress-bar {
            width: 100%;
            height: 4px;
            background: #e0e0e0;
            border-radius: 2px;
            margin: 20px 0;
            overflow: hidden;
            display: none;
        }
        
        .progress-bar.active {
            display: block;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            width: 0%;
            transition: width 0.3s ease;
        }
        
        .spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(102, 126, 234, 0.3);
            border-radius: 50%;
            border-top-color: #667eea;
            animation: spin 1s ease-in-out infinite;
            margin-right: 10px;
            vertical-align: middle;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .feature-list {
            text-align: left;
            margin: 20px 0;
        }
        
        .feature {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
            font-size: 13px;
            color: #333;
        }
        
        .feature-icon {
            margin-right: 10px;
            font-size: 18px;
        }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin: 20px 0;
            border-bottom: 2px solid #e0e0e0;
            overflow-x: auto;
        }
        
        .tab-btn {
            padding: 10px 15px;
            border: none;
            background: none;
            cursor: pointer;
            font-size: 14px;
            color: #666;
            border-bottom: 3px solid transparent;
            transition: all 0.3s ease;
            white-space: nowrap;
        }
        
        .tab-btn.active {
            color: #667eea;
            border-bottom-color: #667eea;
        }
        
        .tab-content {
            display: none;
            animation: fadeIn 0.3s ease;
        }
        
        .tab-content.active {
            display: block;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .files-list {
            text-align: left;
            margin: 20px 0;
        }
        
        .file-item {
            background: #f5f5f5;
            padding: 12px;
            margin-bottom: 8px;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .file-name {
            color: #333;
            font-size: 13px;
            font-weight: 600;
        }
        
        .file-size {
            color: #999;
            font-size: 12px;
        }
        
        .network-info {
            background: #e3f2fd;
            border-left: 4px solid #2196F3;
            padding: 15px;
            margin: 20px 0;
            border-radius: 8px;
            text-align: left;
        }
        
        .network-info p {
            color: #1565c0;
            font-size: 13px;
            line-height: 1.6;
            word-break: break-all;
        }
        
        .code-block {
            background: #263238;
            color: #aed581;
            padding: 12px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            margin: 10px 0;
            overflow-x: auto;
        }
        
        @media (max-width: 480px) {
            .container {
                padding: 30px 20px;
            }
            
            h1 {
                font-size: 24px;
            }
            
            .btn {
                padding: 12px 24px;
                font-size: 15px;
            }
            
            .tabs {
                justify-content: flex-start;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="icon">📱</div>
            <h1>Self-Installer</h1>
            <p class="subtitle">Install the app directly on your device</p>
        </div>
        
        <div class="feature-list">
            <div class="feature">
                <span class="feature-icon">✅</span>
                <span>One-tap installation</span>
            </div>
            <div class="feature">
                <span class="feature-icon">🔄</span>
                <span>Self-updating capability</span>
            </div>
            <div class="feature">
                <span class="feature-icon">📦</span>
                <span>No App Store required</span>
            </div>
        </div>
        
        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab(event, 'install')">📥 Install</button>
            <button class="tab-btn" onclick="switchTab(event, 'guide')">📖 Guide</button>
            <button class="tab-btn" onclick="switchTab(event, 'files')">📄 Files</button>
            <button class="tab-btn" onclick="switchTab(event, 'info')">ℹ️ Info</button>
        </div>
        
        <!-- Install Tab -->
        <div class="tab-content active" id="install">
            <div class="button-group">
                <button class="btn btn-primary" onclick="downloadIPA()">
                    <span id="downloadText">📥 Download IPA</span>
                </button>
                <button class="btn btn-secondary" onclick="downloadManifest()">
                    📄 Download Manifest (Enterprise)
                </button>
            </div>
            
            <div class="progress-bar" id="progressBar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
        </div>
        
        <!-- Guide Tab -->
        <div class="tab-content" id="guide">
            <div class="steps">
                <h3>📱 iPad Installation Steps:</h3>
                <div class="step">
                    <div class="step-number">1</div>
                    <div class="step-text">Click "Download IPA" button</div>
                </div>
                <div class="step">
                    <div class="step-number">2</div>
                    <div class="step-text">The file downloads to your Downloads folder</div>
                </div>
                <div class="step">
                    <div class="step-number">3</div>
                    <div class="step-text">Open the Files app</div>
                </div>
                <div class="step">
                    <div class="step-number">4</div>
                    <div class="step-text">Go to Downloads and find SelfInstaller.ipa</div>
                </div>
                <div class="step">
                    <div class="step-number">5</div>
                    <div class="step-text">Tap the .ipa file to launch installation</div>
                </div>
                <div class="step">
                    <div class="step-number">6</div>
                    <div class="step-text">Confirm installation when prompted</div>
                </div>
                <div class="step">
                    <div class="step-number">7</div>
                    <div class="step-text">App appears on your home screen!</div>
                </div>
            </div>
            
            <div class="info-box">
                <p><strong>💡 Tip:</strong> If you see "Untrusted Developer" warning, go to Settings → General → VPN & Device Management and trust the developer profile.</p>
            </div>
        </div>
        
        <!-- Files Tab -->
        <div class="tab-content" id="files">
            <div class="files-list" id="filesList">
                <p style="color: #999; text-align: center;">Loading files...</p>
            </div>
        </div>
        
        <!-- Info Tab -->
        <div class="tab-content" id="info">
            <div class="info-box">
                <p><strong>App Name:</strong> Self-Installer</p>
                <p><strong>Version:</strong> 1.0.0</p>
                <p><strong>Bundle ID:</strong> com.selfinstaller.app</p>
                <p><strong>Minimum iOS:</strong> 14.0+</p>
                <p id="lastUpdated"><strong>Last Updated:</strong> Just now</p>
            </div>
            
            <div class="info-box" style="border-left-color: #28a745;">
                <p><strong>What does it do?</strong></p>
                <p>This app is designed to install and update itself without needing the App Store. It can download new versions and install them automatically.</p>
            </div>
            
            <div class="info-box" style="border-left-color: #ffc107;">
                <p><strong>⚠️ Important:</strong></p>
                <p>This app requires developer trust on your device. Download only from trusted sources.</p>
            </div>
            
            <div class="network-info">
                <p><strong>🌐 Server Address:</strong></p>
                <p id="serverAddress">Loading...</p>
            </div>
        </div>
        
        <div class="status" id="status"></div>
    </div>
    
    <script>
        function switchTab(event, tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }
        
        function showStatus(message, type = 'info') {
            const statusEl = document.getElementById('status');
            statusEl.textContent = message;
            statusEl.className = 'status ' + type;
            
            // Auto-hide success messages after 5 seconds
            if (type === 'success') {
                setTimeout(() => {
                    statusEl.classList.remove(type);
                }, 5000);
            }
        }
        
        function downloadIPA() {
            const btn = event.target.closest('.btn');
            const textSpan = document.getElementById('downloadText');
            const originalText = textSpan.innerHTML;
            
            // Disable button and show loading
            btn.disabled = true;
            textSpan.innerHTML = '<span class="spinner"></span>Downloading...';
            
            const progressBar = document.getElementById('progressBar');
            const progressFill = document.getElementById('progressFill');
            
            progressBar.classList.add('active');
            progressFill.style.width = '0%';
            
            // Simulate progress
            let progress = 0;
            const interval = setInterval(() => {
                progress += Math.random() * 30;
                progressFill.style.width = Math.min(progress, 90) + '%';
                
                if (progress >= 90) clearInterval(interval);
            }, 200);
            
            // Start actual download
            const link = document.createElement('a');
            link.href = 'SelfInstaller.ipa';
            link.download = 'SelfInstaller.ipa';
            
            setTimeout(() => {
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                
                progressFill.style.width = '100%';
                setTimeout(() => {
                    showStatus('✓ Download started! Check your Files app.', 'success');
                    progressBar.classList.remove('active');
                    btn.disabled = false;
                    textSpan.innerHTML = originalText;
                }, 500);
            }, 1000);
        }
        
        function downloadManifest() {
            const link = document.createElement('a');
            link.href = 'manifest.plist';
            link.download = 'manifest.plist';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            showStatus('✓ Manifest downloaded! Use for enterprise distribution.', 'success');
        }
        
        function loadFiles() {
            fetch('/api/files')
                .then(response => response.json())
                .then(data => {
                    const filesList = document.getElementById('filesList');
                    
                    if (data.files && data.files.length > 0) {
                        filesList.innerHTML = data.files.map(file => `
                            <div class="file-item">
                                <div>
                                    <div class="file-name">📦 ${file.name}</div>
                                    <div class="file-size">${file.size}</div>
                                </div>
                            </div>
                        `).join('');
                    } else {
                        filesList.innerHTML = '<p style="color: #999; text-align: center;">No files available yet</p>';
                    }
                })
                .catch(err => {
                    console.error('Error loading files:', err);
                    document.getElementById('filesList').innerHTML = '<p style="color: #d32f2f;">Error loading files</p>';
                });
        }
        
        function loadServerAddress() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    const addr = document.getElementById('serverAddress');
                    addr.innerHTML = `<strong>http://${window.location.host}</strong><br><em>Server running on: ${data.server_address}</em>`;
                })
                .catch(err => {
                    const addr = document.getElementById('serverAddress');
                    addr.innerHTML = `<strong>http://${window.location.host}</strong>`;
                });
        }
        
        // Update last modified time
        window.addEventListener('load', function() {
            const now = new Date();
            document.getElementById('lastUpdated').innerHTML = 
                `<strong>Last Updated:</strong> ${now.toLocaleString()}`;
            
            loadFiles();
            loadServerAddress();
        });
        
        // Prevent double-click
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('click', function(e) {
                if (this.disabled) return;
                this.style.pointerEvents = 'none';
                setTimeout(() => {
                    this.style.pointerEvents = 'auto';
                }, 1000);
            });
        });
    </script>
</body>
</html>
'''
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def serve_manifest(self):
        """Serve the manifest.plist for enterprise distribution"""
        manifest = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>items</key>
    <array>
        <dict>
            <key>assets</key>
            <array>
                <dict>
                    <key>kind</key>
                    <string>software-package</string>
                    <key>url</key>
                    <string>http://''' + self.headers.get('Host', 'localhost:8000') + '''/SelfInstaller.ipa</string>
                </dict>
            </array>
            <key>metadata</key>
            <dict>
                <key>bundle-identifier</key>
                <string>com.selfinstaller.app</string>
                <key>bundle-version</key>
                <string>1.0.0</string>
                <key>kind</key>
                <string>software</string>
                <key>title</key>
                <string>Self-Installer</string>
            </dict>
        </dict>
    </array>
</dict>
</plist>
'''
        self.send_response(200)
        self.send_header('Content-type', 'application/x-plist')
        self.send_header('Content-Disposition', 'attachment; filename="manifest.plist"')
        self.end_headers()
        self.wfile.write(manifest.encode('utf-8'))
    
    def serve_ipa(self):
        """Serve the IPA file"""
        ipa_path = 'SelfInstaller.ipa'
        if not os.path.exists(ipa_path):
            self.send_error(404, 'IPA file not found. Place SelfInstaller.ipa in the same directory.')
            return
        
        try:
            file_size = os.path.getsize(ipa_path)
            self.send_response(200)
            self.send_header('Content-type', 'application/octet-stream')
            self.send_header('Content-Disposition', 'attachment; filename="SelfInstaller.ipa"')
            self.send_header('Content-Length', file_size)
            self.end_headers()
            
            with open(ipa_path, 'rb') as f:
                self.wfile.write(f.read())
        except Exception as e:
            print(f"Error serving IPA: {e}")
            self.send_error(500, str(e))
    
    def serve_status(self):
        """Serve API status"""
        try:
            host = self.headers.get('Host', 'localhost:8000')
            status = {
                'status': 'online',
                'version': '1.0.0',
                'timestamp': datetime.now().isoformat(),
                'ipa_available': os.path.exists('SelfInstaller.ipa'),
                'server_address': host
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(status).encode('utf-8'))
        except Exception as e:
            self.send_error(500, str(e))
    
    def serve_files_list(self):
        """Serve list of available files"""
        try:
            files = []
            
            # Check for IPA file
            if os.path.exists('SelfInstaller.ipa'):
                size = os.path.getsize('SelfInstaller.ipa')
                size_mb = round(size / (1024 * 1024), 2)
                files.append({
                    'name': 'SelfInstaller.ipa',
                    'size': f'{size_mb} MB',
                    'type': 'ipa'
                })
            
            # Check for manifest
            if os.path.exists('manifest.plist'):
                size = os.path.getsize('manifest.plist')
                size_kb = round(size / 1024, 2)
                files.append({
                    'name': 'manifest.plist',
                    'size': f'{size_kb} KB',
                    'type': 'plist'
                })
            
            response = {
                'status': 'success',
                'files': files,
                'total': len(files)
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception as e:
            self.send_error(500, str(e))
    
    def log_message(self, format, *args):
        """Customize log messages"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}")

def get_ip_address():
    """Get the local IP address"""
    import socket
    try:
        # This works even without internet connection
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def run_server(port=8000, host='0.0.0.0'):
    """Start the web server"""
    server_address = (host, port)
    httpd = HTTPServer(server_address, IPAServerHandler)
    
    local_ip = get_ip_address()
    
    print(f"""
╔════════════════════════════════════════════════════════════╗
║          iOS Self-Installer Web Server v1.0                ║
╚════════════════════════════════════════════════════════════╝

✅ Server is running!

🔗 Access URLs:
   • Local:     http://localhost:{port}
   • Network:   http://{local_ip}:{port}

📱 On your iPad:
   1. Open Safari
   2. Go to: http://{local_ip}:{port}
   3. Tap "Download IPA"
   4. Install from Files app

📦 Files needed:
   • SelfInstaller.ipa (place in same directory as server.py)

⏹️  Press Ctrl+C to stop the server

""")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Server stopped")
        httpd.server_close()

if __name__ == '__main__':
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except:
            print(f"Invalid port: {sys.argv[1]}")
            sys.exit(1)
    
    run_server(port=port)
