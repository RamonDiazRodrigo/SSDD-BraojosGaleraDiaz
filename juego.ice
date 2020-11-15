module Juego {

  exception RoomNotExists{};
  
  interface SerJuego {
    string getRoom() throws RoomNotExists;
  };
  
};
