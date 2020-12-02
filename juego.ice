module Juego {

  exception RoomNotExists{};
  exception Unauthorized {};
  exception RoomAlreadyExists{};
  exception WrongRoomFormat{};
  
  interface SerJuego {
    string getRoom() throws RoomNotExists;
  };

  interface GestMapas {
    void publish(string token, string roomData) throws Unauthorized, RoomAlreadyExists, WrongRoomFormat;
    void remove(string token, string roomName) throws Unauthorized, RoomNotExists;
  };
   interface Authentication {
    void changePassword(string user, string currentPassHash, string newPassHash) throws Unauthorized;
    string getNewToken(string user, string passwordHash) throws Unauthorized;
    bool isValid(string token);
  };
};
