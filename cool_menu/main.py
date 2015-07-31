import util

from state import StateManager, MainMenuState, SettingsState, CreditsState


def main():
    game = StateManager()
    state_dict = {
    	"MainMenu": MainMenuState(),
    	"Settings": SettingsState(),
    	"Credits": CreditsState()
    }
    game.setup_states(state_dict, "MainMenu")
    game.main_loop()

if __name__ == '__main__':
    main()