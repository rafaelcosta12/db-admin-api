package vo

import (
	"testing"
)

func TestNewConnectionString_ValidURL(t *testing.T) {
	raw := "postgres://user:pass@localhost:5432/dbname?sslmode=disable"
	cs, err := NewConnectionString(raw)
	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}
	if cs.String() != raw {
		t.Errorf("Expected %q, got %q", raw, cs.String())
	}
}

func TestNewConnectionString_InvalidURL(t *testing.T) {
	invalid := "://not-a-valid-url"
	_, err := NewConnectionString(invalid)
	if err == nil {
		t.Fatal("Expected error for invalid URL, got nil")
	}
}

func TestConnectionString_String(t *testing.T) {
	raw := "mysql://user:pass@host:3306/db"
	cs, err := NewConnectionString(raw)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if cs.String() != raw {
		t.Errorf("Expected %q, got %q", raw, cs.String())
	}
}
