module rad-tool

go 1.13

require (
	github.com/spf13/cobra v1.0.0
	github.com/yywing/neat/client/neat-client-go v0.0.0-20201011100714-9f0387a48b21
)

replace github.com/yywing/neat/client/neat-client-go => ./../../client/neat-client-go
