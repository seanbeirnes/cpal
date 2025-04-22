/// <reference types="vite/client" />
interface Grecaptcha {
  ready(callback: () => void): void;
  execute(siteKey: string, options: { action: string }): Promise<string>;
}

declare const grecaptcha: Grecaptcha;

