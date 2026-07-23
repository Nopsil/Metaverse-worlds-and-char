$(async () => {
  let done = false;

  async function initVars() {
    if (done) return;
    try {
      await waitGlobalInitialized('Mvu');
      const msgId = getCurrentMessageId();
      const data = Mvu.getMvuData({ type: 'message', message_id: msgId }) || {};

      if (data.stat_data?.selected_character) {
        done = true;
        return;
      }

      // Parse opening from message content
      const msg = SillyTavern.getContext().chat[0]?.mes || '';
      const match = msg.match(/已选择角色[：:]([^，,]+)/);
      const sc = match ? match[1].trim() : null;
      if (!sc) return;

      data.stat_data = {
        selected_character: sc,
        selected_scenario: 0,
        phase: 'playing',
        characters: {
          [sc]: {
            name: sc, affection: 0, relationship: '陌生人',
            mood: '', clothing: '', inner_thought: '',
            body_state: '正常', clothing_integrity: '整齐', pose: '站立'
          }
        }
      };

      await Mvu.replaceMvuData(data, { type: 'message', message_id: msgId });
      done = true;
    } catch (e) {}
  }

  eventOn('MESSAGE_RECEIVED', () => setTimeout(initVars, 800));
  eventOn('MESSAGE_SENT', () => setTimeout(initVars, 800));
  setTimeout(initVars, 2000);
});
