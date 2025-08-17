import React, { useMemo } from 'react';
import { Box, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';

// Import marked for markdown parsing
declare global {
  interface Window {
    marked: any;
    hljs: any;
  }
}

interface MarkdownPreviewProps {
  content: string;
}

const PreviewContainer = styled(Box)(({ theme }) => ({
  flex: 1,
  padding: '16px',
  overflow: 'auto',
  backgroundColor: theme.palette.background.paper,
  
  // Markdown styles
  '& h1, & h2, & h3, & h4, & h5, & h6': {
    marginTop: '24px',
    marginBottom: '16px',
    fontWeight: 600,
    lineHeight: 1.25,
    color: theme.palette.text.primary,
  },
  
  '& h1': {
    fontSize: '2em',
    borderBottom: `1px solid ${theme.palette.divider}`,
    paddingBottom: '8px',
  },
  
  '& h2': {
    fontSize: '1.5em',
    borderBottom: `1px solid ${theme.palette.divider}`,
    paddingBottom: '8px',
  },
  
  '& h3': {
    fontSize: '1.25em',
  },
  
  '& h4': {
    fontSize: '1em',
  },
  
  '& h5': {
    fontSize: '0.875em',
  },
  
  '& h6': {
    fontSize: '0.85em',
    color: theme.palette.text.secondary,
  },
  
  '& p': {
    marginBottom: '16px',
    lineHeight: 1.6,
    color: theme.palette.text.primary,
  },
  
  '& ul, & ol': {
    marginBottom: '16px',
    paddingLeft: '24px',
  },
  
  '& li': {
    marginBottom: '4px',
    lineHeight: 1.6,
  },
  
  '& blockquote': {
    margin: '16px 0',
    padding: '8px 16px',
    borderLeft: `4px solid ${theme.palette.primary.main}`,
    backgroundColor: theme.palette.action.hover,
    fontStyle: 'italic',
    
    '& p': {
      marginBottom: '8px',
    },
  },
  
  '& code': {
    padding: '2px 4px',
    backgroundColor: theme.palette.action.hover,
    borderRadius: '4px',
    fontSize: '0.9em',
    fontFamily: 'JetBrains Mono, Consolas, "Courier New", monospace',
  },
  
  '& pre': {
    margin: '16px 0',
    padding: '16px',
    backgroundColor: theme.palette.background.default,
    borderRadius: '8px',
    overflow: 'auto',
    border: `1px solid ${theme.palette.divider}`,
    
    '& code': {
      padding: 0,
      backgroundColor: 'transparent',
      fontSize: '0.9em',
      lineHeight: 1.4,
    },
  },
  
  '& table': {
    width: '100%',
    marginBottom: '16px',
    borderCollapse: 'collapse',
    border: `1px solid ${theme.palette.divider}`,
  },
  
  '& th, & td': {
    padding: '8px 12px',
    textAlign: 'left',
    borderBottom: `1px solid ${theme.palette.divider}`,
  },
  
  '& th': {
    backgroundColor: theme.palette.action.hover,
    fontWeight: 600,
  },
  
  '& tr:nth-of-type(even)': {
    backgroundColor: theme.palette.action.hover,
  },
  
  '& a': {
    color: theme.palette.primary.main,
    textDecoration: 'none',
    
    '&:hover': {
      textDecoration: 'underline',
    },
  },
  
  '& img': {
    maxWidth: '100%',
    height: 'auto',
    borderRadius: '4px',
    margin: '8px 0',
  },
  
  '& hr': {
    margin: '24px 0',
    border: 'none',
    borderTop: `1px solid ${theme.palette.divider}`,
  },
  
  // Task lists
  '& .task-list-item': {
    listStyle: 'none',
    marginLeft: '-20px',
    
    '& input[type="checkbox"]': {
      marginRight: '8px',
    },
  },
  
  // Highlight.js styles
  '& .hljs': {
    background: theme.palette.background.default,
    color: theme.palette.text.primary,
  },
}));

const MarkdownPreview: React.FC<MarkdownPreviewProps> = ({ content }) => {
  const htmlContent = useMemo(() => {
    if (!content.trim()) {
      return '<p style="color: #888; font-style: italic;">No content to preview</p>';
    }

    try {
      // Configure marked if available
      if (window.marked) {
        window.marked.setOptions({
          highlight: function(code: string, lang: string) {
            if (window.hljs && lang && window.hljs.getLanguage(lang)) {
              try {
                return window.hljs.highlight(code, { language: lang }).value;
              } catch (err) {
                console.warn('Highlight.js error:', err);
              }
            }
            return code;
          },
          breaks: true,
          gfm: true,
        });

        return window.marked.parse(content);
      }
      
      // Fallback: basic markdown-like formatting
      return content
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        .replace(/^\> (.*$)/gim, '<blockquote>$1</blockquote>')
        .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
        .replace(/\*(.*)\*/gim, '<em>$1</em>')
        .replace(/`(.*?)`/gim, '<code>$1</code>')
        .replace(/\n/gim, '<br>');
    } catch (error) {
      console.error('Markdown parsing error:', error);
      return `<p style="color: #f44336;">Error parsing markdown: ${error}</p>`;
    }
  }, [content]);

  return (
    <PreviewContainer>
      {content.trim() ? (
        <div dangerouslySetInnerHTML={{ __html: htmlContent }} />
      ) : (
        <Typography
          variant="body1"
          sx={{
            color: 'text.secondary',
            fontStyle: 'italic',
            textAlign: 'center',
            mt: 4,
          }}
        >
          No content to preview
        </Typography>
      )}
    </PreviewContainer>
  );
};

export default MarkdownPreview;