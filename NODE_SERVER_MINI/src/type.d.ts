declare namespace NodeJS {
  export interface ProcessEnv {
    PORT: string
    NODE_ENV: 'development' | 'production'
  }
}