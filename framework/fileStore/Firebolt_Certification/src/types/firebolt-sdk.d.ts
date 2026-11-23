declare module '*.firebolt-sdk/runner.js' {
  export const runner: {
    run(
      methods: import('../firebolt/SdkAdapter').RunnerEntry[],
      firebolt: import('../firebolt/SdkAdapter').FireboltClient,
      onResult?: (result: import('../firebolt/SdkAdapter').RunnerResult) => void
    ): Promise<{ passed: number; failed: number }>;
  };
}
