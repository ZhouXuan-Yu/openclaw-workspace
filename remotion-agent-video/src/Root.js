import { registerRoot, Composition } from "remotion";
import { RemotionVideo } from "./index";

export const RemotionRoot = () => {
  return (
    <>
      <Composition id="RemotionVideo" component={RemotionVideo} durationInFrames={1236} fps={30} width={1080} height={1920} />
      <Composition id="RemotionVideoPortrait" component={RemotionVideo} durationInFrames={1236} fps={30} width={1080} height={1440} />
    </>
  );
};

registerRoot(RemotionRoot);
