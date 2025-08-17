import React, { forwardRef, useEffect, useRef, useState, useCallback } from 'react';
import { Box, TextareaAutosize } from '@mui/material';
import { styled } from '@mui/material/styles';

interface EditorProps {
  content: string;
  onChange: (content: string) => void;
  settings?: any;
  onCursorPositionChange?: (line: number, column: number) => void;
}

const StyledTextarea = styled(TextareaAutosize)(({ theme }) => ({
  width: '100%',
  height: '100%',
  border: 'none',
  outline: 'none',
  resize: 'none',
  padding: '16px',
  backgroundColor: 'transparent',
  color: theme.palette.text.primary,
  fontFamily: 'JetBrains Mono, Consolas, "Courier New", monospace',
  fontSize: '14px',
  lineHeight: '1.6',
  '&::placeholder': {
    color: theme.palette.text.secondary,
    opacity: 0.7,
  },
  '&::-webkit-scrollbar': {
    width: '8px',
  },
  '&::-webkit-scrollbar-track': {
    background: 'transparent',
  },
  '&::-webkit-scrollbar-thumb': {
    background: theme.palette.divider,
    borderRadius: '4px',
  },
  '&::-webkit-scrollbar-thumb:hover': {
    background: theme.palette.text.secondary,
  },
}));

const LineNumbers = styled(Box)(({ theme }) => ({
  position: 'absolute',
  left: 0,
  top: 0,
  bottom: 0,
  width: '50px',
  backgroundColor: theme.palette.background.default,
  borderRight: `1px solid ${theme.palette.divider}`,
  padding: '16px 8px',
  fontSize: '12px',
  lineHeight: '1.6',
  color: theme.palette.text.secondary,
  fontFamily: 'JetBrains Mono, Consolas, "Courier New", monospace',
  userSelect: 'none',
  overflow: 'hidden',
}));

const Editor = forwardRef<HTMLTextAreaElement, EditorProps>(
  ({ content, onChange, settings, onCursorPositionChange }, ref) => {
    const textareaRef = useRef<HTMLTextAreaElement>(null);
    const [lineNumbers, setLineNumbers] = useState<number[]>([1]);
    const [cursorPosition, setCursorPosition] = useState({ line: 1, column: 1 });

    // Combine refs
    useEffect(() => {
      if (ref && typeof ref === 'object') {
        ref.current = textareaRef.current;
      }
    }, [ref]);

    // Update line numbers when content changes
    useEffect(() => {
      const lines = content.split('\n');
      setLineNumbers(Array.from({ length: lines.length }, (_, i) => i + 1));
    }, [content]);

    // Handle cursor position changes
    const handleSelectionChange = useCallback(() => {
      if (textareaRef.current) {
        const textarea = textareaRef.current;
        const cursorPos = textarea.selectionStart;
        const textBeforeCursor = content.substring(0, cursorPos);
        const lines = textBeforeCursor.split('\n');
        const line = lines.length;
        const column = lines[lines.length - 1].length + 1;
        
        setCursorPosition({ line, column });
        onCursorPositionChange?.(line, column);
      }
    }, [content, onCursorPositionChange]);

    // Handle content change
    const handleChange = useCallback((event: React.ChangeEvent<HTMLTextAreaElement>) => {
      onChange(event.target.value);
    }, [onChange]);

    // Handle key events
    const handleKeyDown = useCallback((event: React.KeyboardEvent<HTMLTextAreaElement>) => {
      const textarea = event.currentTarget;
      
      // Tab handling
      if (event.key === 'Tab') {
        event.preventDefault();
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const tabSize = settings?.tabSize || 2;
        const tab = ' '.repeat(tabSize);
        
        const newContent = content.substring(0, start) + tab + content.substring(end);
        onChange(newContent);
        
        // Set cursor position after tab
        setTimeout(() => {
          textarea.selectionStart = textarea.selectionEnd = start + tab.length;
        }, 0);
      }
      
      // Auto-indent on Enter
      else if (event.key === 'Enter') {
        const start = textarea.selectionStart;
        const lines = content.substring(0, start).split('\n');
        const currentLine = lines[lines.length - 1];
        const indent = currentLine.match(/^\s*/)?.[0] || '';
        
        // Add extra indent for certain patterns
        let extraIndent = '';
        if (currentLine.trim().endsWith(':') || currentLine.trim().endsWith('{')) {
          extraIndent = ' '.repeat(settings?.tabSize || 2);
        }
        
        const newContent = content.substring(0, start) + '\n' + indent + extraIndent + content.substring(textarea.selectionEnd);
        onChange(newContent);
        
        setTimeout(() => {
          textarea.selectionStart = textarea.selectionEnd = start + 1 + indent.length + extraIndent.length;
        }, 0);
        
        event.preventDefault();
      }
      
      // Auto-close brackets and quotes
      else if (['(', '[', '{', '"', "'", '`'].includes(event.key)) {
        const closingChars: { [key: string]: string } = {
          '(': ')',
          '[': ']',
          '{': '}',
          '"': '"',
          "'": "'",
          '`': '`',
        };
        
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const closing = closingChars[event.key];
        
        if (start === end) {
          const newContent = content.substring(0, start) + event.key + closing + content.substring(end);
          onChange(newContent);
          
          setTimeout(() => {
            textarea.selectionStart = textarea.selectionEnd = start + 1;
          }, 0);
          
          event.preventDefault();
        }
      }
    }, [content, onChange, settings]);

    // Handle paste events
    const handlePaste = useCallback((event: React.ClipboardEvent<HTMLTextAreaElement>) => {
      // Allow default paste behavior, but we could add custom handling here
      // For example, formatting pasted code or handling special content types
    }, []);

    // Apply settings
    const editorStyle = {
      fontSize: `${settings?.fontSize || 14}px`,
      fontFamily: settings?.fontFamily === 'monospace' 
        ? 'JetBrains Mono, Consolas, "Courier New", monospace'
        : settings?.fontFamily === 'serif'
        ? 'Georgia, "Times New Roman", serif'
        : settings?.fontFamily === 'sans-serif'
        ? 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
        : 'JetBrains Mono, Consolas, "Courier New", monospace',
      lineHeight: settings?.lineHeight || 1.6,
      whiteSpace: settings?.wordWrap ? 'pre-wrap' : 'pre',
      paddingLeft: settings?.showLineNumbers ? '60px' : '16px',
    };

    return (
      <Box
        sx={{
          position: 'relative',
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
        }}
      >
        {/* Line Numbers */}
        {settings?.showLineNumbers && (
          <LineNumbers>
            {lineNumbers.map((num) => (
              <div key={num} style={{ height: `${(settings?.lineHeight || 1.6) * (settings?.fontSize || 14)}px` }}>
                {num}
              </div>
            ))}
          </LineNumbers>
        )}

        {/* Main Editor */}
        <StyledTextarea
          ref={textareaRef}
          value={content}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          onPaste={handlePaste}
          onSelect={handleSelectionChange}
          onClick={handleSelectionChange}
          onKeyUp={handleSelectionChange}
          placeholder="Start typing your note..."
          style={editorStyle}
          spellCheck={settings?.enableSpellCheck !== false}
        />
      </Box>
    );
  }
);

Editor.displayName = 'Editor';

export default Editor;