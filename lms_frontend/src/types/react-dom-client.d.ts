declare module 'react-dom/client' {
  import type { ReactElement } from 'react';

  interface Root {
    render(children: ReactElement): void;
    unmount(): void;
  }

  export function createRoot(container: Element | DocumentFragment): Root;

  const ReactDOMClient: {
    createRoot: typeof createRoot;
  };
  export default ReactDOMClient;
}
