# Howl - the multi protocol messenger!
The goal of this project is to provided a cli client for multiple message protocols.

This allows logging from bots or remote system using a simple plugin mechanism.

With simple config files (powered by toml) multiple accounts can be maintained side by side withouth the hassle of to many parametrs


## Usage:
Since this project is also powered by fire, you can access all methods defined on the accounts like:

```
./howl.py						# for account listing
./howl.py ACCOUNT send-message	RECIPIENT [MESSAGE] 	# to send message with account
./howl.py ACCOUNT send-receive				# to see all messages	
```
If no message is specified for the send-command, $EDITOR (or the configured one) will be called to create the message

## Configuration:
The default config rests under howl.toml

```
[[account]]
name 	= "My Work account"
...
[[account]]
name	= "My Private account"
...

[logger]
root.level = "DEBUG" # set logging level

[options]
[options.editor]
path	= "/usr/bin/vim"
```

# Contribution
## Messenger-Plugins
All plugins need to inherited from howl.Messenger.Messenger and should implement all listed methods.
To use the plugin, register it by adding it to the howl.toml under the modules section.

## Missing Protocols:
- IRC
- smtp (send only)
- IMAP/POP
- XMPP
- Telegram
- WhatsApp
- Matrix
- Skype
- Threema
- generic binary (stdin-out)

## Feature-TODOs
- contact book
  + using toml
  + using an database interface
- callback mechanism to handle incoming messages actively
- event system to trigger actions on specific content
  + commands for bot usage
  + filter for received messages
- interactive mode
- crypto
- revolver protocol
